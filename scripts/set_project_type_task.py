#!/usr/bin/env python3
"""
Set Project V2 field "Type" to "Task" for issues in a given range.

Targets organization project number 2 for TriResolve-AI. Uses the
GitHub GraphQL API and the environment token `GITHUB_TOKEN` or
`TRIRESOLVE_AUTOMATION_CS_TOKEN`.

Usage:
  export GITHUB_TOKEN="..."
  python3 scripts/set_project_type_task.py --org TriResolve-AI --project-number 2 --repo triresolve-service-desk --start 10 --end 38

The script will:
 - locate the org project by number
 - find the "Type" field and its option id for "Task"
 - for each issue in the range: if the issue is already a project item, update the field; otherwise add the issue to the project then set the field.

"""

import os
import sys
import json
import argparse
import requests

GRAPHQL_URL = "https://api.github.com/graphql"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("TRIRESOLVE_AUTOMATION_CS_TOKEN")


def gql(query, variables=None):
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    resp = requests.post(GRAPHQL_URL, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def find_project(org, number):
    query = """
    query($org: String!, $number: Int!) {
      organization(login: $org) {
        projectV2(number: $number) {
          id
          title
          fields(first: 100) {
            nodes {
              __typename
              ... on ProjectV2SingleSelectField {
                id
                name
                options { id name }
              }
              ... on ProjectV2Field {
                id
                name
              }
            }
          }
          items(first: 250) {
            nodes {
              id
              content {
                ... on Issue { number id }
              }
            }
          }
        }
      }
    }
    """
    res = gql(query, {"org": org, "number": number})
    proj = res.get("organization", {}).get("projectV2")
    if not proj:
        raise RuntimeError(f"Project number {number} not found for org {org}")
    return proj


def add_issue_to_project(project_id, issue_node_id):
    # mutation addProjectV2ItemById
    mut = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input:{projectId:$projectId, contentId:$contentId}) {
        item { id }
      }
    }
    """
    res = gql(mut, {"projectId": project_id, "contentId": issue_node_id})
    return res["addProjectV2ItemById"]["item"]["id"]


def update_field_value(project_id, item_id, field_id, option_id):
    mut = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: String!) {
      updateProjectV2ItemFieldValue(input:{projectId:$projectId, itemId:$itemId, fieldId:$fieldId, value:$value}) {
        projectV2Item { id }
      }
    }
    """
    # value should be JSON string for single-select
    value = json.dumps({"optionId": option_id})
    res = gql(mut, {"projectId": project_id, "itemId": item_id, "fieldId": field_id, "value": value})
    return res


def get_issue_node_id(owner, repo, number):
    q = """
    query($owner: String!, $repo: String!, $number: Int!) {
      repository(owner:$owner, name:$repo) { issue(number:$number) { id } }
    }
    """
    res = gql(q, {"owner": owner, "repo": repo, "number": number})
    issue = res.get("repository", {}).get("issue")
    return issue["id"] if issue else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--org", required=True)
    parser.add_argument("--project-number", type=int, required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()

    if not TOKEN:
        print("GITHUB_TOKEN or TRIRESOLVE_AUTOMATION_CS_TOKEN is required in environment")
        sys.exit(1)

    proj = find_project(args.org, args.project_number)
    project_id = proj["id"]
    print(f"Found project: {proj.get('title')} (id={project_id})")

    # find Type field and Task option
    field_id = None
    task_option_id = None
    for f in proj["fields"]["nodes"]:
        if f["name"].lower() == "type":
            field_id = f["id"]
            options = f.get("options") or []
            for opt in options:
                if opt["name"].lower() == "task":
                    task_option_id = opt["id"]
            break

    if not field_id:
        print("Project field 'Type' not found. Aborting.")
        sys.exit(1)
    if not task_option_id:
        print("Option 'Task' not found in Type field. Aborting.")
        sys.exit(1)

    print(f"Field ID={field_id}, Task option ID={task_option_id}")

    # Map issue number -> item id for items already in project
    item_map = {}
    for node in proj["items"]["nodes"]:
        content = node.get("content")
        if content and "number" in content:
            item_map[int(content["number"])]= node["id"]

    updated = []
    for num in range(args.start, args.end+1):
        try:
            item_id = item_map.get(num)
            if not item_id:
                # add issue to project
                issue_node = get_issue_node_id(args.org, args.repo, num)
                if not issue_node:
                    print(f"Issue #{num} not found in repository; skipping")
                    continue
                print(f"Adding issue #{num} to project")
                item_id = add_issue_to_project(project_id, issue_node)
            # update field to Task
            print(f"Setting Type=Task for issue #{num} (item {item_id})")
            update_field_value(project_id, item_id, field_id, task_option_id)
            updated.append(num)
        except Exception as e:
            print(f"Failed to update issue #{num}: {e}")

    print("Done. Updated issues:", updated)


if __name__ == "__main__":
    main()
