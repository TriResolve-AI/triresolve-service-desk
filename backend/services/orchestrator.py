from backend.api.schemas import (
    AgentResponse,
    TicketCreate,
    TicketResult,
)
from backend.services.classifier import classify_ticket

# Domain agents – these files already live under agents/
# If your agent modules use different function names, adjust imports accordingly.
from agents.it.agent import handle_ticket as it_handle  # type: ignore
from agents.hr.agent import handle_ticket as hr_handle  # type: ignore
from agents.finance.agent import handle_ticket as fin_handle  # type: ignore


def process_ticket(ticket: TicketCreate) -> TicketResult:
    """
    Full pipeline:
    1. Classify ticket into IT / HR / Finance.
    2. Route to the appropriate domain agent.
    3. Return a normalized TicketResult.
    """

    classification = classify_ticket(ticket)

    if classification.department == "IT":
        agent_response: AgentResponse = it_handle(ticket, classification)
    elif classification.department == "HR":
        agent_response = hr_handle(ticket, classification)
    else:
        agent_response = fin_handle(ticket, classification)

    return TicketResult(
        ticket=ticket,
        classification=classification,
        response=agent_response,
    )
