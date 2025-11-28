# backend/api/services/orchestrator.py

import os

from backend.api.schemas import (
    AgentResponse,
    TicketCreate,
    TicketResult,
)
from backend.services.classifier import classify_ticket
from backend.services.azure_client import chat_completion

# Name of the orchestrator deployment in Azure Foundry
ORCHESTRATOR_MODEL = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR",
    None,  # falls back to settings.azure_openai_model if not set
)


def _build_user_prompt(ticket: TicketCreate) -> str:
    """
    Turn the incoming ticket into a clean text block for the LLM.
    """
    return (
        f"Ticket title: {ticket.title}\n"
        f"Description: {ticket.description}\n"
        f"Priority: {ticket.priority}\n"
    )


def process_ticket(ticket: TicketCreate) -> TicketResult:
    """
    Full pipeline (LLM-backed orchestrator version):

    1. Classify ticket into IT / HR / Finance.
    2. Call the TriResolve Orchestrator LLM deployment.
    3. Return a normalized TicketResult that the UI already understands.
    """
    # Step 1: classify
    classification = classify_ticket(ticket)

    # Step 2: call orchestrator deployment
    system_prompt = (
        "You are the TriResolve Orchestrator Agent. "
        "You receive IT / HR / Finance service desk tickets and coordinate "
        "between specialist agents and tools (abstracted away from you here). "
        "Return a clear, actionable response for the requester. "
        "Always explain what is happening, what will be done, and the next steps."
    )

    user_prompt = _build_user_prompt(ticket)

    answer = chat_completion(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=ORCHESTRATOR_MODEL,
        temperature=0.4,  # a little more creative than default 0.2
        max_tokens=1200,
    )

    # Step 3: wrap into your existing AgentResponse / TicketResult types
    agent_response = AgentResponse(
        agent_name="TriResolve Orchestrator",
        department=classification.department,
        summary=answer,
        steps=answer,  # you can later parse into separate steps if you want
    )

    return TicketResult(
        ticket=ticket,
        classification=classification,
        response=agent_response,
    )
