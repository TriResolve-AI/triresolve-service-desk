"""
Basic tests for the FastAPI backend
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path to import backend module
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns correct response"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "TriResolve" in data["message"]


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_list_agents():
    """Test listing available agents"""
    response = client.get("/api/agents")
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
    assert len(data["agents"]) == 3
    
    # Check all three agent categories are present
    categories = [agent["category"] for agent in data["agents"]]
    assert "IT" in categories
    assert "HR" in categories
    assert "Finance" in categories


def test_create_ticket():
    """Test creating a new ticket"""
    ticket_data = {
        "title": "Test Ticket",
        "description": "This is a test ticket for IT support",
        "category": "IT",
        "priority": "high"
    }
    
    response = client.post("/api/tickets", json=ticket_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "created"
    assert "ticket_id" in data
    assert "IT" in data["message"]
