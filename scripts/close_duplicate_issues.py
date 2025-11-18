import os
import requests
from collections import defaultdict
from datetime import datetime

# Close duplicate issues by exact title. Keeps the oldest issue and closes newer duplicates.

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "TriResolve-AI"
REPO = "triresolve-service-desk"

if not GITHUB_TOKEN:
    raise SystemExit("❌ Please set GITHUB_TOKEN environment variable.")

API_BASE = f"https://api.github.com/repos/{OWNER}/{REPO}"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def fetch_all_issues():
    issues = []
    page = 1
    per_page = 100
    while True:
        url = f"{API_BASE}/issues?state=all&per_page={per_page}&page={page}"
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            raise SystemExit(f"Failed to list issues: {resp.status_code} {resp.text}")
        batch = resp.json()
        if not batch:
            break
        issues.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return issues


def close_issue(number, keep_number):
    comment_url = f"{API_BASE}/issues/{number}/comments"
    body = {"body": f"Closing as duplicate of #{keep_number}."}
    c = requests.post(comment_url, headers=HEADERS, json=body)
    if c.status_code not in (200, 201):
        print(f"⚠️ Failed to post comment on #{number}: {c.status_code} {c.text}")

    patch_url = f"{API_BASE}/issues/{number}"
    p = requests.patch(patch_url, headers=HEADERS, json={"state": "closed"})
    if p.status_code == 200:
        print(f"🔒 Closed issue #{number} (duplicate of #{keep_number})")
    else:
        print(f"❌ Failed to close #{number}: {p.status_code} {p.text}")


def iso_to_dt(s):
    try:
        return datetime.fromisoformat(s.replace('Z', '+00:00'))
    except Exception:
        return datetime.min


def main():
    print("Scanning issues for duplicate titles...")
    issues = fetch_all_issues()

    # Filter out pull requests (issues with `pull_request` key)
    issues = [i for i in issues if 'pull_request' not in i]

    title_map = defaultdict(list)
    for i in issues:
        title = i.get('title', '').strip()
        title_map[title].append(i)

    duplicates_found = 0
    for title, group in title_map.items():
        if not title:
            continue
        if len(group) <= 1:
            continue
        # Sort by creation time (oldest first)
        group_sorted = sorted(group, key=lambda x: iso_to_dt(x.get('created_at', '')))
        keep = group_sorted[0]
        keep_number = keep.get('number')
        print(f"Found {len(group_sorted)} issues with title: '{title}' — keeping #{keep_number}")
        for dup in group_sorted[1:]:
            dup_number = dup.get('number')
            if dup.get('state') == 'closed':
                print(f"- Skipping #{dup_number} (already closed)")
                continue
            close_issue(dup_number, keep_number)
            duplicates_found += 1

    if duplicates_found == 0:
        print("No open duplicate issues found.")
    else:
        print(f"Done. Closed {duplicates_found} duplicate issues.")


if __name__ == '__main__':
    main()
