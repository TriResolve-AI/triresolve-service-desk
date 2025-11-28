"""
TriNexa Ops Agent – Python stub.
"""

from backend.api.schemas import AgentResponse, TicketCreate, TicketClassification


def handle(ticket: TicketCreate, classification: TicketClassification) -> AgentResponse:
    """
    Placeholder Ops handler.

    Returns a basic guidance message so that the pipeline has a safe default
    until real Ops logic is integrated.
    """
    return AgentResponse(
        agent_name="ops",
        department="Operations",
        summary=(
            "Ops stub: an on-call engineer should review the incident details, "
            "consult runbooks, and verify system health."
        ),
        steps=(
            "1. Check key dashboards and alerts. "
            "2. Follow relevant runbooks. "
            "3. Escalate to the owning service team if unresolved."
        ),
    )
