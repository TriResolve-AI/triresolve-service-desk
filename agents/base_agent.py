"""
Base Agent Class
Provides common functionality for all TriResolve AI agents
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel


class AgentConfig(BaseModel):
    """Configuration for an agent"""
    name: str
    category: str
    description: str
    enabled: bool = True


class TicketData(BaseModel):
    """Ticket data structure"""
    ticket_id: str
    title: str
    description: str
    category: str
    priority: str = "medium"
    status: str = "open"


class AgentResponse(BaseModel):
    """Response from an agent"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class BaseAgent:
    """Base class for all agents in TriResolve AI"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.name = config.name
        self.category = config.category
    
    async def process_ticket(self, ticket: TicketData) -> AgentResponse:
        """
        Process a ticket and return a response
        To be implemented by specific agent subclasses
        """
        raise NotImplementedError("Subclasses must implement process_ticket method")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": self.name,
            "category": self.category,
            "enabled": self.config.enabled,
            "status": "active" if self.config.enabled else "inactive"
        }
