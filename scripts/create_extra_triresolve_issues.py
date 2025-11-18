#!/usr/bin/env python3
"""
Create a set of repository issues via the GitHub REST API.

This script uses the `GITHUB_TOKEN` environment variable. It targets
the `TriResolve-AI/triresolve-service-desk` repository and will create
each issue defined in `EXTRA_ISSUES`. If assignees are rejected by the
API (422 validation), it will retry creating the issue without assignees.

Usage (Codespaces / local):

export GITHUB_TOKEN="<your-token>"
python3 scripts/create_extra_triresolve_issues.py

Note: Do NOT hardcode a token into this file or commit secrets to the repo.
"""

import os
import requests
from typing import Dict, Any

REPO = "TriResolve-AI/triresolve-service-desk"
TOKEN = os.environ.get("GITHUB_TOKEN")
API_URL = "https://api.github.com"

# 🔁 Replace these with real GitHub usernames if needed
ASSIGNEE_PORTIA = "portiajefferson"
ASSIGNEE_MEGAN = "megan-nepshinsky"
ASSIGNEE_ESTEFANY = "GITHUB_USERNAME_ESTEFANY"
ASSIGNEE_NITHYA = "GITHUB_USERNAME_NITHYA"

EXTRA_ISSUES = [
    {
        "title": "Write AGENTS.md – document IT / HR / Finance agent prompts & roles",
        "body": (
            "Create docs/AGENTS.md documenting:\n"
            "- Each agent (IT, HR, Finance)\n"
            "- Purpose and responsibilities\n"
            "- Prompt structure and key guardrails\n"
            "- Example inputs/outputs\n"
        ),
        "labels": ["Task", "type: documentation", "priority: medium"],
        "assignees": [ASSIGNEE_PORTIA],
    },
    {
        "title": "Create QUICKSTART.md – how to run the demo locally in Codespaces",
        "body": (
            "Add a QUICKSTART.md that explains:\n"
            "- Pre-requisites (Codespaces, Python version, env vars)\n"
            "- How to start the FastAPI backend\n"
            "- How to open the frontend / demo page\n"
            "- Common troubleshooting steps\n"
        ),
        "labels": ["Task", "type: documentation", "priority: high"],
        "assignees": [ASSIGNEE_MEGAN],
    },
    {
        "title": "Add smoke tests for each agent route (IT / HR / Finance)",
        "body": (
            "Add basic tests that hit each agent route and assert a 200 response:\n"
            "- /tickets/it\n"
            "- /tickets/hr\n"
            "- /tickets/finance\n"
            "Include at least one minimal payload per route."
        ),
        "labels": ["Task", "type: backend", "priority: medium"],
        "assignees": [ASSIGNEE_MEGAN],
    },
    {
        "title": "Add happy-path end-to-end test: submit ticket → agent → resolution",
        "body": (
            "Implement an automated test that:\n"
            "1. Creates a sample ticket via the FastAPI endpoint\n"
            "2. Routes it through the domain classifier\n"
            "3. Invokes the correct agent\n"
            "4. Asserts a non-empty resolution response\n"
        ),
        "labels": ["Task", "type: testing", "priority: medium"],
        "assignees": [ASSIGNEE_PORTIA],
    },
    {
        "title": "Write script/notebook to generate synthetic tickets from templates",
        "body": (
            "Create a small script or notebook that generates synthetic tickets for:\n"
            "- IT (password reset, access request, VPN, laptop issue)\n"
            "- HR (PTO, benefits, payroll question)\n"
            "- Finance (invoice, reimbursement, vendor payment)\n"
            "Output data as JSON or CSV that can be used for testing/demo."
        ),
        "labels": ["Task", "type: data", "priority: medium"],
        "assignees": [ASSIGNEE_PORTIA],
    },
    {
        "title": "Polish ticket submission UI (validation, error messages, success banner)",
        "body": (
            "Improve the ticket submission form UX:\n"
            "- Required field validation with inline errors\n"
            "- Clear error message if backend fails\n"
            "- Success banner with ticket ID when created\n"
        ),
        "labels": ["Task", "type: frontend", "priority: medium"],
        "assignees": [ASSIGNEE_ESTEFANY],
    },
    {
        "title": "Add loading states and error toasts for agent visualizer and results",
        "body": (
            "In the frontend, add:\n"
            "- Loading indicators while agent chain runs\n"
            "- Error toasts when something fails\n"
            "- Disabled buttons while a run is in progress\n"
        ),
        "labels": ["Task", "type: frontend", "priority: low"],
        "assignees": [ASSIGNEE_ESTEFANY],
    },
    {
        "title": "Create demo runbook for judges (step-by-step sequence)",
        "body": (
            "Document the exact demo flow for judges:\n"
            "- Which synthetic ticket to submit\n"
            "- What they should see at each stage\n"
            "- Key talking points for each agent\n"
            "- Fallback plan if something fails live\n"
        ),
        "labels": ["Task", "epic: presentation", "type: documentation", "priority: high"],
        "assignees": [ASSIGNEE_NITHYA],
    },
    {
        "title": "Capture final screenshots and diagrams for the slide deck",
        "body": (
            "Capture visual assets for the presentation:\n"
            "- Screenshot of ticket submission UI\n"
            "- Screenshot of agent reasoning visualizer\n"
            "- High-level architecture diagram\n"
            "Store them under docs/assets/ or a similar folder."
        ),
        "labels": ["Task", "epic: presentation", "type: design", "priority: medium"],
        "assignees": [ASSIGNEE_NITHYA, ASSIGNEE_ESTEFANY],
    },
]


def create_issue(issue: Dict[str, Any]) -> None:
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    payload = {
        "title": issue["title"],
        "body": issue["body"],
        "labels": issue.get("labels", []),
        "assignees": [a for a in issue.get("assignees", []) if a],
    }

    resp = requests.post(f"{API_URL}/repos/{REPO}/issues", json=payload, headers=headers)

    # If assignees are invalid, retry without assignees
    if resp.status_code == 422 and "assignees" in resp.text:
        payload["assignees"] = []
        resp = requests.post(f"{API_URL}/repos/{REPO}/issues", json=payload, headers=headers)

    resp.raise_for_status()
    data = resp.json()
    print(f"Created #{data['number']}: {data['title']}")


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("GITHUB_TOKEN environment variable is required.")

    for issue in EXTRA_ISSUES:
        try:
            create_issue(issue)
        except Exception as exc:
            print(f"Failed to create issue '{issue.get('title')}' - {exc}")
