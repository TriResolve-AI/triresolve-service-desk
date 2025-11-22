#!/usr/bin/env python3
"""
Create milestones for the TriResolve AI hackathon project.

This script creates the following milestones via the GitHub REST API:
- M1 – Foundations Ready
- M2 – Backend Routing + Agents
- M3 – Classifier + API
- M4 – Demo UX & Storyboard
- M5 – Full System Demo
- M6 – Final Submission

Usage:
  export GITHUB_TOKEN="..."
  python3 scripts/create_milestones.py
"""

import os
import requests
from typing import Dict, List, Any

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "TriResolve-AI"
REPO = "triresolve-service-desk"
API_TIMEOUT = 30  # seconds

if not GITHUB_TOKEN:
    raise SystemExit("❌ Please set GITHUB_TOKEN environment variable.")

API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/milestones"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

# Milestone definitions
MILESTONES = [
    {
        "title": "M1 – Foundations Ready",
        "description": "Core repository setup, tooling, and documentation foundations are in place.",
        "state": "open",
    },
    {
        "title": "M2 – Backend Routing + Agents",
        "description": "Backend API is functional with agent routing and domain classification.",
        "state": "open",
    },
    {
        "title": "M3 – Classifier + API",
        "description": "Domain classifier is trained/integrated and API endpoints are complete.",
        "state": "open",
    },
    {
        "title": "M4 – Demo UX & Storyboard",
        "description": "Demo UI and presentation storyboard are ready for rehearsal.",
        "state": "open",
    },
    {
        "title": "M5 – Full System Demo",
        "description": "End-to-end system demonstration is working and rehearsed.",
        "state": "open",
    },
    {
        "title": "M6 – Final Submission",
        "description": "All deliverables complete and submitted for hackathon judging.",
        "state": "open",
    },
]


def create_milestone(milestone: Dict[str, Any]) -> None:
    """Create a single milestone via GitHub API."""
    payload = {
        "title": milestone["title"],
        "description": milestone.get("description", ""),
        "state": milestone.get("state", "open"),
    }
    
    resp = requests.post(API_URL, json=payload, headers=HEADERS, timeout=API_TIMEOUT)
    
    if resp.status_code == 201:
        data = resp.json()
        print(f"✅ Created milestone: {data['title']} (#{data['number']})")
        print(f"   URL: {data['html_url']}")
    elif resp.status_code == 422:
        # Milestone might already exist or validation error occurred
        try:
            data = resp.json()
            errors = data.get("errors", [])
            # Check if any error indicates the milestone already exists
            already_exists = any(
                "already_exists" in str(e).lower() or 
                "already exists" in str(e).lower()
                for e in errors
            )
            if already_exists:
                print(f"⚠️  Milestone already exists: {milestone['title']}")
            else:
                print(f"❌ Failed to create milestone: {milestone['title']}")
                print(f"   Status: {resp.status_code}")
                print(f"   Errors: {errors}")
        except Exception as e:
            print(f"❌ Failed to create milestone: {milestone['title']}")
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text}")
    else:
        print(f"❌ Failed to create milestone: {milestone['title']}")
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {resp.text}")


def list_existing_milestones() -> List[str]:
    """Fetch existing milestone titles from the repository."""
    try:
        resp = requests.get(API_URL, headers=HEADERS, params={"state": "all"}, timeout=API_TIMEOUT)
        if resp.status_code == 200:
            milestones = resp.json()
            return [m["title"] for m in milestones]
        else:
            print(f"⚠️  Warning: Failed to fetch existing milestones (status {resp.status_code})")
            return []
    except Exception as e:
        print(f"⚠️  Warning: Error fetching existing milestones: {e}")
        return []


def main():
    print(f"Creating milestones for {OWNER}/{REPO}...\n")
    
    # Check for existing milestones
    existing = list_existing_milestones()
    if existing:
        print(f"ℹ️  Found {len(existing)} existing milestone(s): {', '.join(existing)}\n")
    
    # Create each milestone
    for milestone in MILESTONES:
        if milestone["title"] in existing:
            print(f"⏭️  Skipping (already exists): {milestone['title']}")
        else:
            create_milestone(milestone)
    
    print("\n✅ Milestone creation complete!")


if __name__ == "__main__":
    main()
