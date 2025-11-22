#!/usr/bin/env python3
"""
Add Milestone field with options to GitHub Project V2.

This script adds a single-select "Milestone" field to the specified
GitHub Project V2 with the following options:
- M1 – Foundations Ready
- M2 – Backend Routing + Agents
- M3 – Classifier + API
- M4 – Demo UX & Storyboard
- M5 – Full System Demo
- M6 – Final Submission

Usage:
  export GITHUB_TOKEN="..."
  python3 scripts/add_project_milestone_field.py --org TriResolve-AI --project-number 2
"""

import os
import sys
import argparse
import requests

GRAPHQL_URL = "https://api.github.com/graphql"
TOKEN = os.environ.get("GITHUB_TOKEN")


def gql(query, variables=None):
    """Execute a GraphQL query."""
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    resp = requests.post(GRAPHQL_URL, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    
    return data["data"]


def find_project(org, number):
    """Find a GitHub Project V2 by organization and project number."""
    query = """
    query($org: String!, $number: Int!) {
      organization(login: $org) {
        projectV2(number: $number) {
          id
          title
          fields(first: 100) {
            nodes {
              __typename
              ... on ProjectV2Field {
                id
                name
              }
              ... on ProjectV2SingleSelectField {
                id
                name
                options { id name }
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


def create_milestone_field(project_id, milestone_options):
    """
    Create a single-select Milestone field in the project.
    
    Note: As of now, the GitHub GraphQL API does not support creating
    custom fields programmatically. This must be done through the GitHub UI.
    
    This function serves as a placeholder/documentation for the manual steps.
    """
    print("⚠️  GitHub Projects V2 API does not currently support creating custom fields via GraphQL.")
    print("ℹ️  Please create the 'Milestone' field manually through the GitHub UI:")
    print()
    print("   1. Go to your GitHub Project")
    print("   2. Click on '+' to add a new field")
    print("   3. Choose 'Single select' as the field type")
    print("   4. Name it 'Milestone'")
    print("   5. Add the following options:")
    for i, option in enumerate(milestone_options, 1):
        print(f"      - {option}")
    print()
    print("   Alternatively, if API support is added, this script can be updated.")
    
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Add Milestone field to GitHub Project V2"
    )
    parser.add_argument("--org", required=True, help="Organization name")
    parser.add_argument("--project-number", type=int, required=True, help="Project number")
    args = parser.parse_args()
    
    if not TOKEN:
        print("❌ GITHUB_TOKEN environment variable is required")
        sys.exit(1)
    
    milestone_options = [
        "M1 – Foundations Ready",
        "M2 – Backend Routing + Agents",
        "M3 – Classifier + API",
        "M4 – Demo UX & Storyboard",
        "M5 – Full System Demo",
        "M6 – Final Submission",
    ]
    
    print(f"Finding project in {args.org}, number {args.project_number}...")
    proj = find_project(args.org, args.project_number)
    project_id = proj["id"]
    print(f"✅ Found project: {proj['title']} (id={project_id})")
    
    # Check if Milestone field already exists
    existing_fields = {f["name"]: f for f in proj["fields"]["nodes"]}
    
    if "Milestone" in existing_fields:
        field = existing_fields["Milestone"]
        print(f"\n✅ Milestone field already exists (id={field['id']})")
        
        if field["__typename"] == "ProjectV2SingleSelectField":
            existing_options = [opt["name"] for opt in field.get("options", [])]
            print(f"   Current options: {', '.join(existing_options)}")
            
            missing = set(milestone_options) - set(existing_options)
            if missing:
                print(f"\n⚠️  Missing options: {', '.join(missing)}")
                print("   Please add these manually through the GitHub UI")
            else:
                print("\n✅ All milestone options are already configured!")
        else:
            print(f"   ⚠️  Warning: Field exists but is not a single-select field (type: {field['__typename']})")
    else:
        print("\n📝 Milestone field does not exist yet.")
        create_milestone_field(project_id, milestone_options)


if __name__ == "__main__":
    main()
