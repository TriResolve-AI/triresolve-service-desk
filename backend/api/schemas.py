# backend/api/schemas.py
from typing import Literal, Optional

from pydantic import BaseModel, Field

Department = Literal["IT", "HR", "Finance"]
Priority = Literal["Low", "Medium", "High", "Critical"]
Domain = Literal["it", "hr", "finance", "security", "architect", "ops"]


class TicketCreate(BaseModel):
    title: str = Field(..., example="Cannot log into email")
    description: str = Field(
        ...,
        example="I forgot my password and Outlook is saying my credentials are invalid.",
    )
    priority: Priority = "Medium"


class TicketClassification(BaseModel):
    department: Department
    confidence: float = Field(..., ge=0.0, le=1.0)
    rationale: str


class AgentResponse(BaseModel):
    agent_name: str
    department: Department
    summary: str
    steps: str


class TicketResult(BaseModel):
    """
    Full pipeline result: input ticket, classification, and agent response.
    """

    ticket: TicketCreate
    classification: TicketClassification
    response: AgentResponse


# ==============================
# Chat-based API for Streamlit
# ==============================


class ChatRequest(BaseModel):
    """
    Generic chat-style request for the TriResolve Assistant.

    `domain` is optional:
      - If provided ("it", "hr", "finance", "security", "architect", "ops"),
        the backend will route directly to that domain agent.
      - If omitted, the orchestrator will decide how to route.
    """

    message: str = Field(
        ...,
        example="My VPN keeps disconnecting when I work from home.",
    )
    domain: Optional[Domain] = Field(
        default=None,
        description="Optional domain override.",
    )


class ChatResponse(BaseModel):
    """
    Simple chat-style response returned to the Streamlit UI.
    """

    reply: str
