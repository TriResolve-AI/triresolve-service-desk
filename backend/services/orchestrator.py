# backend/api/services/orchestrator.py

import os

from backend.api.schemas import (
    AgentResponse,
    TicketCreate,
    TicketResult,
    TicketClassification,
)
from backend.services.classifier import classify_ticket
from backend.services.azure_client import chat_completion

# Config settings (DEV_MODE toggle, etc.)
from config import settings

# Name of the orchestrator deployment in Azure
ORCHESTRATOR_MODEL = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR",
    None,  # falls back to settings.d_orchestrator if not set
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


def process_ticket(ticket: TicketCreate, force_dev: bool = False) -> TicketResult:
    """
    Full pipeline (LLM-backed orchestrator version):

    1. Classify ticket into IT / HR / Finance.
    2. Call the TriResolve Orchestrator LLM deployment.
    3. Return a normalized TicketResult that the UI already understands.
    """
    # Short-circuit in dev mode with a deterministic canned response.
    if getattr(settings, "DEV_MODE", False) or force_dev:
        classification = TicketClassification(
            department="IT",
            confidence=0.95,
            rationale="Dev mode – static output.",
        )

        agent_response = AgentResponse(
            agent_name="TriResolve Orchestrator (dev)",
            department="IT",
            summary="Dev mode response – everything working!",
            steps="This is a demo response.",
        )

        return TicketResult(ticket=ticket, classification=classification, response=agent_response)

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

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    answer = chat_completion(
        messages=messages,
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
