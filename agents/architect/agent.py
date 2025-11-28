"""
TriNexa Architect Agent – Python stub.

This module exists mainly as a placeholder so the repo has a consistent
structure across agents. The backend orchestration currently lives in:

    backend/services/orchestrator.py

In the future, this module can be expanded to host any Python-side helper
logic specific to the Architect agent.
"""

from backend.api.schemas import AgentResponse, TicketCreate, TicketClassification


def handle(ticket: TicketCreate, classification: TicketClassification) -> AgentResponse:
    """
    Placeholder Architect handler.

    Right now this returns a static response so that tests or demo calls
    do not fail. When we introduce dedicated architect flows, this
    function can call Azure OpenAI using the Architect agent profile.
    """
    return AgentResponse(
        agent_name="architect",
        department="Architecture",
        summary=(
            "Architect stub: a detailed architecture response will be provided "
            "once the Architect agent is fully wired into the backend."
        ),
        steps="1. Review ticket. 2. Design architecture. 3. Return plan.",
    )
