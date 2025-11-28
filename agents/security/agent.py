"""
TriNexa Security Agent – Python stub.
"""

from backend.api.schemas import AgentResponse, TicketCreate, TicketClassification


def handle(ticket: TicketCreate, classification: TicketClassification) -> AgentResponse:
    """
    Placeholder Security handler.

    Returns a minimal, safe response until the Security agent is wired into
    the LLM orchestration and tools.
    """
    return AgentResponse(
        agent_name="security",
        department="Security",
        summary=(
            "Security stub: this ticket should be evaluated by the Security "
            "agent and/or human security reviewer in a future iteration."
        ),
        steps=(
            "1. Review data sensitivity and access. "
            "2. Verify alignment with security policies. "
            "3. Escalate to Security team if needed."
        ),
    )
