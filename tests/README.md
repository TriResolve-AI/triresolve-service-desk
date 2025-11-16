# Tests

This directory contains all test files for the TriResolve AI Service Desk application.

## Test Structure

### Unit Tests
- `test_agents/`: Tests for individual agent functionality
- `test_backend/`: Tests for backend API endpoints
- `test_models/`: Tests for data models and schemas

### Integration Tests
- End-to-end workflows
- Agent orchestration
- API integration tests

### Test Data
- Mock ticket data
- Test configurations
- Sample responses

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov=agents

# Run specific test file
pytest tests/test_backend/test_main.py
```

## Writing Tests
- Follow the existing test structure
- Use descriptive test names
- Include docstrings explaining test purpose
- Aim for high code coverage
- Test both success and failure cases
