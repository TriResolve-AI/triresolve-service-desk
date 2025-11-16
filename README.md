# TriResolve AI Service Desk

Multi-agent service desk orchestrator for IT, HR, and Finance ticket auto-resolution powered by AI.

## Overview

TriResolve AI is an intelligent service desk automation platform that uses multiple specialized AI agents to automatically resolve common IT, HR, and Finance support tickets. The system leverages LangChain and large language models to understand, categorize, and resolve tickets with minimal human intervention.

## Features

- 🤖 **Multi-Agent Architecture**: Specialized agents for IT, HR, and Finance departments
- ⚡ **FastAPI Backend**: High-performance async API server
- 🔄 **Auto-Resolution**: Intelligent ticket routing and automated resolution
- 📊 **Analytics Ready**: Built-in support for tracking and reporting
- 🔌 **Extensible**: Easy to add new agents and capabilities

## Project Structure

```
triresolve-service-desk/
├── backend/           # FastAPI backend server
│   ├── main.py       # Main API application
│   └── __init__.py
├── agents/           # AI agent implementations
│   ├── base_agent.py    # Base agent class
│   ├── it_agent.py      # IT support agent
│   ├── hr_agent.py      # HR support agent
│   ├── finance_agent.py # Finance support agent
│   └── __init__.py
├── frontend/         # Web frontend (planned)
├── runbooks/         # Operational procedures and workflows
├── data/            # Application data and configurations
├── docs/            # Project documentation
├── tests/           # Test files
└── requirements.txt # Python dependencies
```

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/TriResolve-AI/triresolve-service-desk.git
cd triresolve-service-desk
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the backend server:
```bash
cd backend
python main.py
```

Or using uvicorn directly:
```bash
uvicorn backend.main:app --reload
```

4. Access the API:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## API Endpoints

- `GET /` - Root endpoint with API status
- `GET /health` - Health check endpoint
- `POST /api/tickets` - Create a new support ticket
- `GET /api/agents` - List available agents

## Agent Categories

### IT Support Agent
Handles:
- Password resets
- Software installation requests
- Hardware troubleshooting
- Network issues

### HR Support Agent
Handles:
- Leave applications
- Benefits queries
- Onboarding requests
- Policy questions

### Finance Support Agent
Handles:
- Expense reimbursements
- Invoice queries
- Budget questions
- Payment status

## Development

### Running Tests
```bash
pytest
```

### Code Structure
- Each agent extends the `BaseAgent` class
- Agents use Pydantic models for data validation
- Async/await pattern for all operations

## Roadmap

- [ ] Implement LLM integration for intelligent ticket analysis
- [ ] Add vector database for knowledge base
- [ ] Build web frontend interface
- [ ] Implement user authentication and authorization
- [ ] Add real-time notifications
- [ ] Integrate with popular ticketing systems (Jira, ServiceNow, etc.)
- [ ] Add analytics dashboard
- [ ] Implement learning from ticket resolutions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details.

## Support

For questions or support, please open an issue on GitHub.
