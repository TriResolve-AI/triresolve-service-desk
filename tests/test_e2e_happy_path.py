from fastapi.testclient import TestClient

from backend.api.main import app  # adjust import if your app path is different

client = TestClient(app)


def test_e2e_it_happy_path():
    """
    Happy-path E2E:
    submit ticket -> backend /orchestrator -> classifier + IT agent -> resolution JSON
    """
    payload = {
        "ticket": "I can't log into my laptop after the VPN change. "
                  "It keeps saying my password is incorrect."
    }

    response = client.post("/orchestrator", json=payload)
    assert response.status_code == 200

    data = response.json()

    # Depending on how your orchestrator returns:
    # Example if backend returns { "response": { ...orchestrator_output... } }
    assert "response" in data

    orchestrator_output = data["response"]

    # These keys should line up with what we defined in the orchestrator contract
    # e.g.:
    # {
    #   "final_answer": "...",
    #   "agents_consulted": [...],
    #   "actions_taken": "...",
    #   "next_steps": "...",
    #   "risk_escalation": "..."
    # }

    assert isinstance(orchestrator_output, dict)
    assert "final_answer" in orchestrator_output
    assert isinstance(orchestrator_output["final_answer"], str)
    assert orchestrator_output["final_answer"].strip() != ""

    # Optional sanity checks
    if "agents_consulted" in orchestrator_output:
        assert "it" in [a.lower() for a in orchestrator_output["agents_consulted"]]
