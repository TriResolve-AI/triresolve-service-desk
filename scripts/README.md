# Scripts Directory

This directory contains automation scripts for managing the TriResolve AI project.

## Milestone Management Scripts

### create_milestones.py
Creates the six project milestones in the GitHub repository via the REST API.

**Usage:**
```bash
export GITHUB_TOKEN="your_token"
python3 scripts/create_milestones.py
```

**Creates:**
- M1 – Foundations Ready
- M2 – Backend Routing + Agents
- M3 – Classifier + API
- M4 – Demo UX & Storyboard
- M5 – Full System Demo
- M6 – Final Submission

### add_project_milestone_field.py
Checks for and guides creation of a "Milestone" field in GitHub Projects V2.

**Usage:**
```bash
export GITHUB_TOKEN="your_token"
python3 scripts/add_project_milestone_field.py --org TriResolve-AI --project-number 2
```

**Note:** GitHub API doesn't support programmatic field creation. This script validates existing configuration and provides instructions for manual setup.

## Issue Management Scripts

### create_extra_triresolve_issues.py
Creates additional task issues for the project.

### close_duplicate_issues.py
Utility for closing duplicate issues.

### retry_assign_nithya.py
Retries issue assignment operations.

## Project Management Scripts

### set_project_type_task.py
Sets the "Type" field to "Task" for issues in a specified range within a GitHub Project V2.

**Usage:**
```bash
export GITHUB_TOKEN="your_token"
python3 scripts/set_project_type_task.py \
  --org TriResolve-AI \
  --project-number 2 \
  --repo triresolve-service-desk \
  --start 10 \
  --end 38
```

## Prerequisites

All scripts require:
- Python 3.7+
- `requests` library (`pip install requests`)
- GitHub Personal Access Token with appropriate permissions
  - For milestones: `repo` scope
  - For projects: `project` scope

## Environment Variables

Set your GitHub token:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

Or for some scripts:
```bash
export TRIRESOLVE_AUTOMATION_CS_TOKEN="ghp_your_token_here"
```
