# backend/api/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.api.schemas import (
    TicketCreate,
    TicketResult,
    ChatRequest,
    ChatResponse,
)
from backend.services.orchestrator import process_ticket
from backend.services.azure_client import (
    orchestrator_chat,
    domain_agent_chat,
)

app = FastAPI(
    title="TriResolve Service Desk API",
    version="0.1.0",
    description="Backend API for TriResolve / TriNexa multi-agent service desk.",
)

# Allow Streamlit frontend + local tools to call this API.
# You can tighten origins later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    """
    Simple healthcheck endpoint for debugging / probes.
    """
    return {"status": "ok"}


@app.post("/tickets/process", response_model=TicketResult)
def process_ticket_endpoint(payload: TicketCreate, request: Request) -> TicketResult:
    """
    Ingest a ticket, classify it, and call the TriResolve Orchestrator
    Azure OpenAI deployment. Returns the full structured result the UI expects.
    """
    force_dev = request.query_params.get("dev") in {"1", "true", "True"}
    return process_ticket(payload, force_dev=force_dev)


@app.post("/orchestrator")
def orchestrator_endpoint(payload: dict) -> dict:
    """
    Backwards-compatible test/dev endpoint used by integration tests and
    lightweight clients. Accepts a JSON body like `{ "ticket": "..." }`.

    Returns a small `response` object with keys the tests expect.
    """
    ticket_text = payload.get("ticket", "")

    # Build a minimal TicketCreate from the free-text payload so we can reuse
    # the existing `process_ticket` pipeline.
    ticket = TicketCreate(title=(ticket_text[:50] or "ticket"), description=ticket_text, priority="Medium")

    # This lightweight `/orchestrator` test endpoint should use dev-mode
    # behaviour to avoid calling external Azure services during tests.
    result = process_ticket(ticket, force_dev=True)

    orchestrator_output = {
        "final_answer": result.response.summary,
        "agents_consulted": [result.response.department],
        "actions_taken": "",
        "next_steps": result.response.steps,
    }

    return {"response": orchestrator_output}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """
    Chat-style endpoint for the TriResolve Assistant (used by Streamlit).

    - If `payload.domain` is provided ("it", "hr", "finance", etc.), we route
      directly to that domain agent using Azure OpenAI.
    - If `payload.domain` is omitted or None, we call the orchestrator and let
      it decide how to coordinate agents.
    """
    if payload.domain:
        reply = domain_agent_chat(payload.message, domain=payload.domain)
    else:
        reply = orchestrator_chat(payload.message)

    return ChatResponse(reply=reply)
