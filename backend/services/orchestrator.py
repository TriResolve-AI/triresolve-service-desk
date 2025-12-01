import os
import json

from backend.api.schemas import (
    AgentResponse,
    TicketCreate,
    TicketResult,
    TicketClassification,
)
from backend.services.classifier import classify_ticket
from backend.services.azure_client import chat_completion

from config import settings  # DEV_MODE etc.

ORCHESTRATOR_MODEL = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR",
    None,  # falls back to settings.d_orchestrator if not set
)

SYSTEM_PROMPT = """
Role
You are TriNexa, the TriResolve Orchestrator Agent for the AI Service Desk.
You receive a classified ticket and act as the central brain and final responder.

You do not call other agents directly in this version; instead, you reason about
what the specialist agents (HR, IT, Finance, Architect, Security, Ops) would do
and synthesize their guidance.

Inputs
You receive a JSON object with:

{
  "ticket": {
    "title": "...",
    "description": "...",
    "priority": "Low | Medium | High | Critical"
  },
  "classification": {
    "department": "IT | HR | Finance | Internal",
    "confidence": 0.0-1.0,
    "rationale": "..."
  }
}

Responsibilities

1. Route logically (reasoning only)
Decide which domain is responsible: Finance, HR, IT, Architect, Security, or Ops.

Use routing rules:
- Finance → reimbursements, invoices, expenses, corporate card, vendor payments
- HR → PTO, leave, onboarding/offboarding, benefits, policy questions
- IT → access, MFA, email, hardware, VPN, network/app issues
- Architect → system design, workflows, integrations, scalability
- Security → risk, access control, suspicious activity, policy enforcement
- Ops → incidents, outages, reliability, operational runbooks

2. Generate a structured employee response

Produce an employee_response object:

"employee_response": {
  "category": "Finance | HR | IT | Security | Ops | Architect",
  "topic": "...",
  "decision": "...",
  "summary": "...",
  "policy_reference": "...",
  "next_step": "..."
}

- summary: 2–4 sentences explaining what is happening.
- next_step: clear action for the employee (and/or IT/HR/etc.).

3. Log orchestration details for internal use

Produce an orchestration_log object:

"orchestration_log": {
  "agents_consulted": ["classifier", "it"],
  "actions_taken": [
    "Classifier determined department = IT and priority = High",
    "TriNexa generated IT response based on VPN access runbook"
  ],
  "risk_or_escalation": "None"  // or explanation if Security/Ops would escalate
}

4. Create a final, user-facing answer

Additionally return a final_answer string that the UI can display directly:

"final_answer": "Natural-language explanation in 3–6 sentences, written to the employee."

- Do NOT mention internal agent names in final_answer.
- Use a professional, friendly tone.

Output Format

Always return ONLY a single JSON object with this exact top-level structure:

{
  "employee_response": {
    "category": "...",
    "topic": "...",
    "decision": "...",
    "summary": "...",
    "policy_reference": "...",
    "next_step": "..."
  },
  "orchestration_log": {
    "agents_consulted": ["classifier", "..."],
    "actions_taken": ["..."],
    "risk_or_escalation": "..."
  },
  "final_answer": "..."
}
"""


def _build_orchestrator_input(ticket: TicketCreate, classification: TicketClassification) -> str:
    """
    Build the JSON payload that we describe in the system prompt.
    """
    payload = {
        "ticket": {
            "title": ticket.title,
            "description": ticket.description,
            "priority": ticket.priority,
        },
        "classification": {
            "department": classification.department,
            "confidence": classification.confidence,
            "rationale": classification.rationale,
        },
    }
    return json.dumps(payload, ensure_ascii=False)


def process_ticket(ticket: TicketCreate, force_dev: bool = False) -> TicketResult:
    """
    Full pipeline (TriNexa-style orchestrator):

    1. Classify ticket into IT / HR / Finance / Internal.
    2. Call the TriNexa Orchestrator deployment with structured JSON.
    3. Parse the JSON response and map into TicketResult.
    """
    # Dev-mode short-circuit
    if getattr(settings, "DEV_MODE", False) or force_dev:
        classification = TicketClassification(
            department="IT",
            confidence=0.95,
            rationale="Dev mode – static output.",
        )

        agent_response = AgentResponse(
            agent_name="TriNexa Orchestrator (dev)",
            department="IT",
            summary="Dev mode response – everything working!",
            steps="This is a demo response.",
        )

        return TicketResult(ticket=ticket, classification=classification, response=agent_response)

    # Step 1: classify (via classifier agent deployment)
    classification = classify_ticket(ticket)

    # Step 2: call orchestrator deployment with structured payload
    orchestrator_input = _build_orchestrator_input(ticket, classification)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Here is the ticket and classification JSON:\n\n{orchestrator_input}",
        },
    ]

    raw = chat_completion(
        messages=messages,
        model=ORCHESTRATOR_MODEL,
        temperature=0.4,
        max_tokens=1200,
    )

    # Be defensive: extract JSON block only
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        # Fallback: treat whole answer as plain text
        agent_response = AgentResponse(
            agent_name="TriNexa Orchestrator",
            department=classification.department,
            summary=raw,
            steps=raw,
        )
        return TicketResult(ticket=ticket, classification=classification, response=agent_response)

    data = json.loads(raw[start : end + 1])

    employee_response = data.get("employee_response", {}) or {}
    final_answer = data.get("final_answer") or employee_response.get("summary") or raw

    agent_response = AgentResponse(
        agent_name="TriNexa Orchestrator",
        department=classification.department,
        summary=final_answer,
        steps=employee_response.get("next_step") or final_answer,
    )

    return TicketResult(
        ticket=ticket,
        classification=classification,
        response=agent_response,
    )
