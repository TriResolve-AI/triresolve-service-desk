"""
TriResolve AI - Multi-Agent Service Desk
FastAPI Backend Server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="TriResolve AI Service Desk",
    description="Multi-agent service desk orchestrator for IT, HR, and Finance ticket auto-resolution",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    message: str


class TicketRequest(BaseModel):
    title: str
    description: str
    category: str  # IT, HR, or Finance
    priority: str = "medium"


class TicketResponse(BaseModel):
    ticket_id: str
    status: str
    message: str


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse(
        status="ok",
        message="TriResolve AI Service Desk API is running"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="All systems operational"
    )


@app.post("/api/tickets", response_model=TicketResponse)
async def create_ticket(ticket: TicketRequest):
    """Create a new service desk ticket"""
    # Placeholder for ticket creation logic
    # In production, this would route to appropriate agents
    return TicketResponse(
        ticket_id="TICKET-001",
        status="created",
        message=f"Ticket created for {ticket.category} category"
    )


@app.get("/api/agents")
async def list_agents():
    """List available agents"""
    return {
        "agents": [
            {"name": "IT Support Agent", "category": "IT", "status": "active"},
            {"name": "HR Support Agent", "category": "HR", "status": "active"},
            {"name": "Finance Support Agent", "category": "Finance", "status": "active"}
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
