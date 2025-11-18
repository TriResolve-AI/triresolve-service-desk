#!/usr/bin/env python3
"""
Retry assigning issues #37 and #38 to Nithya when she accepts the collaborator invite.

This script checks whether `Nithyananthisenthilkumar` is a collaborator on the
repository `TriResolve-AI/triresolve-service-desk`. If so, it assigns issues #37
and #38 to her, removes the `status: needs triage` and `owner: nithya` labels,
and ensures `status: backlog` and `type: Task` are present. It will also post a
comment noting the assignment.

Run locally or from CI. The repository's `GITHUB_TOKEN` (or a token with issue
permissions) must be available in the environment.
"""

import os
import sys
import requests
from typing import List

REPO = "TriResolve-AI/triresolve-service-desk"
USERNAME = "Nithyananthisenthilkumar"
ISSUES = [37, 38]

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("TRIRESOLVE_AUTOMATION_CS_TOKEN")
API_URL = "https://api.github.com"


def api_headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    }


def is_collaborator(username: str) -> bool:
    url = f"{API_URL}/repos/{REPO}/collaborators/{username}"
    resp = requests.get(url, headers=api_headers())
    if resp.status_code == 204:
        return True
    if resp.status_code == 404:
        return False
    resp.raise_for_status()
    return False


def add_labels(issue: int, labels: List[str]) -> None:
    url = f"{API_URL}/repos/{REPO}/issues/{issue}/labels"
    resp = requests.post(url, json=labels, headers=api_headers())
    resp.raise_for_status()


def remove_label(issue: int, label: str) -> None:
    # label must be URL-encoded when calling the delete endpoint
    from urllib.parse import quote_plus

    url = f"{API_URL}/repos/{REPO}/issues/{issue}/labels/{quote_plus(label)}"
    resp = requests.delete(url, headers=api_headers())
    # 404 means label wasn't present — ignore
    if resp.status_code not in (200, 204, 404):
        resp.raise_for_status()


def assign_issue(issue: int, assignees: List[str]) -> None:
    url = f"{API_URL}/repos/{REPO}/issues/{issue}/assignees"
    resp = requests.post(url, json={"assignees": assignees}, headers=api_headers())
    # If the assignee invite isn't accepted yet, API may return 422 — raise for others
    if resp.status_code == 201 or resp.status_code == 200:
        return
    if resp.status_code == 422:
        # validation error (likely not a collaborator yet)
        raise RuntimeError(f"Cannot assign #{issue}: {resp.status_code} {resp.text}")
    resp.raise_for_status()


def post_comment(issue: int, body: str) -> None:
    url = f"{API_URL}/repos/{REPO}/issues/{issue}/comments"
    resp = requests.post(url, json={"body": body}, headers=api_headers())
    resp.raise_for_status()


def main():
    if not TOKEN:
        print("GITHUB_TOKEN is required in environment.")
        sys.exit(1)

    print(f"Checking whether {USERNAME} is a collaborator...")
    try:
        collab = is_collaborator(USERNAME)
    except Exception as e:
        print("Failed to check collaborator status:", e)
        sys.exit(1)

    if not collab:
        print(f"{USERNAME} is not a collaborator yet. Exiting; will retry later.")
        sys.exit(2)

    print(f"{USERNAME} is a repository collaborator — assigning issues...")

    for issue in ISSUES:
        try:
            assign_issue(issue, [USERNAME])
            # tidy labels
            try:
                remove_label(issue, "status: needs triage")
            except Exception:
                pass
            try:
                remove_label(issue, "owner: nithya")
            except Exception:
                pass
            add_labels(issue, ["status: backlog", "type: Task"])
            post_comment(issue, f"Assigned to @{USERNAME} after collaborator invite accepted; moving to Backlog.")
            print(f"Assigned and updated labels for #{issue}")
        except Exception as e:
            print(f"Failed to assign/update #{issue}: {e}")


if __name__ == "__main__":
    main()
