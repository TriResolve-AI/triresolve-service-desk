from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api")

class Ticket(BaseModel):
	title: str
	description: str
	category: str  # it, hr, finance


@router.post("/classify")
def classify_ticket(ticket: Ticket):
	return {"category": ticket.category, "status": "classification complete"}

