import json

from backend.api.schemas import TicketCreate, TicketClassification
from backend.services.azure_client import chat_completion

SYSTEM_PROMPT = """
Role
You are the TriResolve Classifier Agent.
Your job is to identify the correct domain for incoming employee queries so the Orchestrator can route them to the appropriate Employee Agent (Finance, HR, IT).

Do not provide policy explanations or solutions.
Focus only on domain classification and optional clarifying questions.

Responsibilities

Receive query inputs:
- ticket_id (optional in this pipeline)
- user / user_profile (optional)
- issue_description (we will derive this from title + description)
- urgency (mapped from ticket priority)
- manager (optional, often not provided)

Determine the domain:
- Finance → reimbursements, invoices, corporate card, budgets, procurement
- HR → PTO, leave, benefits, onboarding/offboarding, policies, training
- IT → technical issues, devices, accounts, VPN, software, hardware
- Internal → Security, Ops, Architect, or other internal system / platform requests

Return classification with confidence level:
Use a value between 0.0 and 1.0 to indicate confidence.

Output Format
ALWAYS return ONLY valid JSON with this exact shape:

{
  "ticket_id": "<ticket_id or null>",
  "domain": "<Finance | HR | IT | Internal>",
  "confidence": 0.0-1.0,
  "clarifying_question": "<optional, null if confident>"
}

Behavior Guidelines
- Do not resolve queries – classification only.
- Analyze the combined title + description + priority to determine domain.
- Keep classification consistent, auditable, and concise.
- Avoid guessing – request clarification if unsure (confidence < 0.8).
- Maintain neutral, professional language.
"""


def classify_ticket(ticket: TicketCreate) -> TicketClassification:
    """
    Use Azure OpenAI (deployed classifier agent) to classify a ticket into IT, HR, Finance, or Internal.
    """

    # Map our TicketCreate into the "issue_description" + urgency concept
    issue_description = f"Title: {ticket.title}\nDescription: {ticket.description}"
    urgency = ticket.priority  # Low | Medium | High | Critical

    user_prompt = f"""
ticket_id: null
issue_description:
{issue_description}

urgency: {urgency}
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    raw = chat_completion(messages)

    # Be defensive in case the model adds extra prose
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"Classifier returned non-JSON output: {raw}")

    data = json.loads(raw[start : end + 1])

    # Map Foundry-style "domain" back into your existing TicketClassification model
    # Your Department type today is Literal["IT", "HR", "Finance"], so we coerce Internal if needed.
    domain = data.get("domain", "IT")
    if domain.lower() == "internal":
        # Default ambiguous "Internal" into IT for now, or you can choose Finance/HR.
        mapped_department = "IT"
    else:
        mapped_department = domain.upper()

    return TicketClassification(
        department=mapped_department,  # "IT" | "HR" | "FINANCE" (you can normalize if needed)
        confidence=float(data.get("confidence", 0.7)),
        rationale=data.get("clarifying_question") or data.get("rationale", ""),
    )
