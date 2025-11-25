#!/usr/bin/env bash
set -euo pipefail

BRANCH="normalize-backend-structure"
BASE="main"

echo "Fetching ${BASE}..."
git fetch origin ${BASE}
git checkout -b ${BRANCH} origin/${BASE}

# Ensure services dir exists
mkdir -p backend/services

# Move/rename only if files exist
if [ -f backend/api/models/ticket.py ]; then
  mkdir -p backend/api/models
  git mv backend/api/models/ticket.py backend/api/schemas.py || cp backend/api/models/ticket.py backend/api/schemas.py
fi

if [ -f backend/utils/classifier.py ]; then
  mkdir -p backend/services
  git mv backend/utils/classifier.py backend/services/classifier.py || cp backend/utils/classifier.py backend/services/classifier.py
fi

if [ -f backend/services/resolver.py ]; then
  git mv backend/services/resolver.py backend/services/orchestrator.py || cp backend/services/resolver.py backend/services/orchestrator.py
fi

# Overwrite/create files with the exact contents you provided
cat > backend/config.py <<'PY'
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Central configuration for the backend.

    Values are pulled from environment variables and optionally a .env file
    in the repo root.
    """

    # Azure OpenAI
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str = "2024-02-15-preview"
    azure_openai_model: str = "gpt-4o-mini"  # or your AOAI deployment name

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
PY

cat > backend/services/azure_client.py <<'PY'
from openai import AzureOpenAI

from backend.config import get_settings

settings = get_settings()

# Single shared Azure OpenAI client
client = AzureOpenAI(
    api_key=settings.azure_openai_api_key,
    api_version=settings.azure_openai_api_version,
    azure_endpoint=settings.azure_openai_endpoint,
)


def chat_completion(system_prompt: str, user_prompt: str, model: str | None = None) -> str:
    """
    Helper that wraps Azure OpenAI chat completions.

    Returns the string content of the first choice.
    """
    model_name = model or settings.azure_openai_model

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
PY

cat > backend/api/schemas.py <<'PY'
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
PY

cat > backend/services/classifier.py <<'PY'
import json

from backend.api.schemas import TicketCreate, TicketClassification
from backend.services.azure_client import chat_completion

SYSTEM_PROMPT = """
You are a router for a multi-department service desk.

Your job is to classify each ticket into exactly ONE department:
- IT
- HR
- Finance

Always return ONLY valid JSON with this shape:

{
  "department": "IT" | "HR" | "Finance",
  "confidence": 0.0-1.0,
  "rationale": "short explanation"
}
"""


def classify_ticket(ticket: TicketCreate) -> TicketClassification:
    """
    Use Azure OpenAI to classify a ticket into IT, HR, or Finance.
    """

    user_prompt = f"""
Title: {ticket.title}
Description: {ticket.description}
Priority: {ticket.priority}
"""

    raw = chat_completion(SYSTEM_PROMPT, user_prompt)

    # Be defensive in case the model adds extra prose
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"Classifier returned non-JSON output: {raw}")

    data = json.loads(raw[start : end + 1])

    return TicketClassification(
        department=data["department"],
        confidence=float(data.get("confidence", 0.7)),
        rationale=data.get("rationale", ""),
    )
PY

cat > backend/services/orchestrator.py <<'PY'
from backend.api.schemas import (
    AgentResponse,
    TicketCreate,
    TicketResult,
)
from backend.services.classifier import classify_ticket

# Domain agents – these files already live under agents/
# If your agent modules use different function names, adjust imports accordingly.
from agents.it.agent import handle_ticket as it_handle  # type: ignore
from agents.hr.agent import handle_ticket as hr_handle  # type: ignore
from agents.finance.agent import handle_ticket as fin_handle  # type: ignore


def process_ticket(ticket: TicketCreate) -> TicketResult:
    """
    Full pipeline:
    1. Classify ticket into IT / HR / Finance.
    2. Route to the appropriate domain agent.
    3. Return a normalized TicketResult.
    """

    classification = classify_ticket(ticket)

    if classification.department == "IT":
        agent_response: AgentResponse = it_handle(ticket, classification)
    elif classification.department == "HR":
        agent_response = hr_handle(ticket, classification)
    else:
        agent_response = fin_handle(ticket, classification)

    return TicketResult(
        ticket=ticket,
        classification=classification,
        response=agent_response,
    )


💡 Note:
If your existing agents/*/agent.py files don’t yet have a handle_ticket(ticket, classification) function, we can add small wrappers later. For now, this defines the contract the orchestrator expects.
PY

cat > backend/api/main.py <<'PY'
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
PY

cat > backend/main.py <<'PY'
"""
Thin wrapper so you can run:

    uvicorn backend.main:app --reload

and still keep the real FastAPI app in backend/api/main.py
"""

from backend.api.main import app  # noqa: F401
PY

# Update imports across the repo (careful: review before committing)
# Replace backend.api.models.ticket -> backend.api.schemas
git grep -l "backend.api.models.ticket" || true | xargs -r sed -i 's|backend.api.models.ticket|backend.api.schemas|g'

# Replace backend.utils.classifier -> backend.services.classifier
git grep -l "backend.utils.classifier" || true | xargs -r sed -i 's|backend.utils.classifier|backend.services.classifier|g'

# Replace backend.services.resolver -> backend.services.orchestrator
git grep -l "backend.services.resolver" || true | xargs -r sed -i 's|backend.services.resolver|backend.services.orchestrator|g'

# Optionally ensure top-level imports reference the expected symbols if needed:
# (run these only if you want to force replacement of many import shapes; inspect outputs)
# git grep -n "from backend.api.models" || true
# git grep -n "backend.services.resolver" || true

# Add, commit, push
git add -A
git commit -m "Normalize backend structure: move, rename, and replace files"
git push -u origin ${BRANCH}

# Create PR using gh (GitHub CLI). If you don't have gh installed, open the PR in the web UI.
if command -v gh >/dev/null 2>&1; then
  gh pr create --base ${BASE} --title "Normalize backend structure: move, rename, and replace files" --body "Move/rename files, replace backend files with normalized structure, and update imports. Do not modify streamlit/ or agents/." 
else
  echo "gh CLI not found; create a PR from ${BRANCH} -> ${BASE} with title: Normalize backend structure: move, rename, and replace files"
fi

echo "Done. If 'gh pr create' ran, it will prompt you to confirm; otherwise open a PR in the web UI from ${BRANCH} -> ${BASE}."
