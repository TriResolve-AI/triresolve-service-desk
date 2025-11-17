from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api", tags=["tickets"])

class Ticket(BaseModel):
    subject: str
    description: str
    user_id: Optional[str] = None
    priority: Optional[str] = "medium"

class TicketResponse(BaseModel):
    ticket_id: str
    domain: str
    agent: str
    status: str
    resolution: Optional[str] = None

@router.post("/classify", response_model=TicketResponse)
async def classify_ticket(ticket: Ticket):
    """
    Classify incoming ticket and route to appropriate agent
    """
    # Simple classification logic (to be enhanced with ML model)
    domain = "IT"  # Default domain
    agent = "IT Agent"
    
    # Basic keyword matching for demonstration
    description_lower = ticket.description.lower()
    
    if any(word in description_lower for word in ["password", "vpn", "login", "access", "device"]):
        domain = "IT"
        agent = "IT Agent"
    elif any(word in description_lower for word in ["pto", "leave", "benefits", "hr", "policy"]):
        domain = "HR"
        agent = "HR Agent"
    elif any(word in description_lower for word in ["payroll", "invoice", "reimbursement", "budget", "finance"]):
        domain = "Finance"
        agent = "Finance Agent"
    
    return TicketResponse(
        ticket_id="TKT-001",
        domain=domain,
        agent=agent,
        status="classified",
        resolution=None
    )

@router.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    """
    Retrieve ticket status and resolution
    """
    return {
        "ticket_id": ticket_id,
        "status": "in_progress",
        "message": "Ticket retrieval endpoint"
    }
