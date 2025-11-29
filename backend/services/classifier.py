import json

from backend.api.schemas import TicketCreate, TicketClassification
from backend.services.azure_client import chat_completion

SYSTEM_PROMPT = """
You are a router for a multi-department service desk.

Your job is to classify each ticket into exactly ONE department:
- IT
- HR
- Finance

Always return ONLY valid JSON with this shape:

{
  "department": "IT" | "HR" | "Finance",
  "confidence": 0.0-1.0,
  "rationale": "short explanation"
}
"""


def classify_ticket(ticket: TicketCreate) -> TicketClassification:
    """
    Use Azure OpenAI to classify a ticket into IT, HR, or Finance.
    """

    user_prompt = f"""
Title: {ticket.title}
Description: {ticket.description}
Priority: {ticket.priority}
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

    return TicketClassification(
        department=data["department"],
        confidence=float(data.get("confidence", 0.7)),
        rationale=data.get("rationale", ""),
    )
