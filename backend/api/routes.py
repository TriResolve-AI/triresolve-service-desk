# backend/api/routes.py

from fastapi import APIRouter

from .schemas import OrchestratorTicket, OrchestratorResponse
from .services.orchestrator import run_orchestrator

router = APIRouter()


@router.post("/orchestrate", response_model=OrchestratorResponse)
async def orchestrate_ticket(ticket: OrchestratorTicket) -> OrchestratorResponse:
    """
    Accepts a ticket payload and returns the Orchestrator's response.

    This is the main entrypoint the UI / Streamlit app should call
    when a user submits a service desk request.
    """
    result_text = run_orchestrator(ticket.model_dump())
    return OrchestratorResponse(answer=result_text)
