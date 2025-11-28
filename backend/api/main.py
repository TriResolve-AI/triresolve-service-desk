# backend/api/main.py

from fastapi import FastAPI
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
def process_ticket_endpoint(payload: TicketCreate) -> TicketResult:
    """
    Ingest a ticket, classify it, and call the TriResolve Orchestrator
    Azure OpenAI deployment. Returns the full structured result the UI expects.
    """
    return process_ticket(payload)


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
