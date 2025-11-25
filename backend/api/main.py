from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.schemas import TicketCreate, TicketResult
from backend.services.orchestrator import process_ticket

app = FastAPI(
    title="TriResolve Service Desk API",
    version="0.1.0",
    description="Backend API for TriResolve / TriNexa multi-agent service desk.",
)

# Allow Streamlit frontend + local tools to call this API.
# You can tighten origins later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    """
    Simple healthcheck endpoint for debugging / probes.
    """
    return {"status": "ok"}


@app.post("/tickets/process", response_model=TicketResult)
def process_ticket_endpoint(payload: TicketCreate) -> TicketResult:
    """
    Ingest a ticket, classify it, route to the appropriate agent,
    and return the full structured result.
    """
    return process_ticket(payload)
