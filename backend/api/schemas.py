from typing import Literal

from pydantic import BaseModel, Field

Department = Literal["IT", "HR", "Finance"]
Priority = Literal["Low", "Medium", "High", "Critical"]


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
