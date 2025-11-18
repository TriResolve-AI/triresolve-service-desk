import os
import requests
from textwrap import dedent

# -----------------------------
# CONFIG
# -----------------------------
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "TriResolve-AI"
REPO = "triresolve-service-desk"

if not GITHUB_TOKEN:
    raise SystemExit("❌ Please set GITHUB_TOKEN environment variable.")

API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


# GitHub usernames
ASSIGNEES = {
    "portia": "portiajefferson",
    "esthefany": "steffahv",
    "nithya": "Nithyananthisenthilkumar",
    "megan": "megan-nepshinsky",
}

# -----------------------------
# ISSUE DEFINITIONS
# -----------------------------

ISSUES = [

    # EPIC 0 – Meta / Coordination
    {
        "title": "[Meta] Finalize hackathon scope & success criteria",
        "body": dedent("""
            ## Summary
            Align on final scope for the TriResolve AI project and what "success" looks like for this hackathon.

            ## Tasks
            - Confirm which flows must be fully working (IT/HR/Finance)
            - Define what we will SHOW in the demo vs what will be conceptual
            - Decide timeline for code freeze and slide freeze
            - Capture decisions in Notion + Slack #announcements

            ## Acceptance Criteria
            - Documented scope in Notion
            - Everyone in the team acknowledges the final scope in Slack
        """).strip(),
        "labels": ["epic: meta", "priority: high", "type: planning"],
        "assignees": [ASSIGNEES["portia"]],
    },

    # EPIC 1 – Repo & Tooling
    {
        "title": "Set up repo conventions & CONTRIBUTING.md",
        "body": dedent("""
            ## Summary
            Finalize coding conventions, branching, and contribution rules for TriResolve.

            ## Tasks
            - Review CONTRIBUTING.md
            - Make sure branch naming & commit style are documented
            - Link to issue & PR templates
            - Announce in Slack #ux-docs or #eng-core

            ## Acceptance Criteria
            - CONTRIBUTING.md is merged into `main`
            - Team knows where to find contribution rules
        """).strip(),
        "labels": ["epic: repo", "priority: medium", "type: documentation"],
        "assignees": [ASSIGNEES["portia"]],
    },
    {
        "title": "Wire up basic CI workflow for lint + tests (optional)",
        "body": dedent("""
            ## Summary
            Add a lightweight GitHub Actions workflow to run linting and tests.

            ## Tasks
            - Create `.github/workflows/ci.yml`
            - Run `pytest` (if tests exist) and at least `python -m compileall` or `ruff`/`flake8` if configured
            - Ensure workflow runs on PRs and pushes to `main`

            ## Acceptance Criteria
            - CI passes for `main`
            - New PRs show CI status checks
        """).strip(),
        "labels": ["epic: repo", "priority: low", "type: automation"],
        "assignees": [ASSIGNEES["esthefany"]],
    },

    # EPIC 2 – Backend & API
    {
        "title": "Implement FastAPI ticket intake endpoint",
        "body": dedent("""
            ## Summary
            Build the main `/tickets` endpoint to accept user tickets.

            ## Tasks
            - Define Pydantic model for ticket input (title, description, category, urgency)
            - Implement route handler in `backend/main.py`
            - Basic validation and error handling
            - Return a structured ticket ID + status

            ## Acceptance Criteria
            - Endpoint callable via `curl` or HTTPie
            - Request/response shapes documented in `docs/api-reference.md`
        """).strip(),
        "labels": ["epic: backend", "priority: high", "type: backend"],
        "assignees": [ASSIGNEES["esthefany"]],
    },
    {
        "title": "Implement domain classifier call in backend",
        "body": dedent("""
            ## Summary
            Connect ticket intake to the domain classifier (IT/HR/Finance).

            ## Tasks
            - Add classifier service or module
            - Map model output to internal enums: `IT`, `HR`, `FINANCE`
            - Handle low-confidence predictions (e.g., fallback or ask-for-more-info flag)
            - Log decisions for debugging

            ## Acceptance Criteria
            - Ticket submitted via API is classified into IT/HR/Finance
            - Logs show input, prediction, and confidence
        """).strip(),
        "labels": ["epic: backend", "priority: high", "type: backend"],
        "assignees": [ASSIGNEES["esthefany"], ASSIGNEES["nithya"]],
    },
    {
        "title": "Wire backend to agent router (IT / HR / Finance agents)",
        "body": dedent("""
            ## Summary
            After domain classification, route tickets to the appropriate agent entrypoint.

            ## Tasks
            - Implement agent router module
            - Define contract between backend and each agent (input schema, expected output)
            - Add error handling and fallback for agent failures

            ## Acceptance Criteria
            - For sample tickets, backend calls correct agent module
            - Router logic is unit-tested or at least smoke-tested
        """).strip(),
        "labels": ["epic: backend", "priority: high", "type: backend"],
        "assignees": [ASSIGNEES["esthefany"]],
    },

    # EPIC 3 – Agents & Runbooks
    {
        "title": "Design IT/HR/Finance agent prompts & roles",
        "body": dedent("""
            ## Summary
            Define prompts, instructions, and responsibilities for each domain agent.

            ## Tasks
            - Write base system prompts for IT, HR, and Finance agents
            - Specify what tools/runbooks each agent can call
            - Capture edge cases (escalation, missing data, out-of-scope requests)

            ## Acceptance Criteria
            - Prompts are versioned in `agents/` or `docs/agent-guide.md`
            - At least one example conversation per agent documented
        """).strip(),
        "labels": ["epic: agents", "priority: high", "type: design"],
        "assignees": [ASSIGNEES["nithya"], ASSIGNEES["portia"]],
    },
    {
        "title": "Implement IT agent logic with runbook execution",
        "body": dedent("""
            ## Summary
            Implement the IT agent that can execute YAML runbooks (e.g., password reset).

            ## Tasks
            - Load IT runbooks from `runbooks/it/`
            - Map runbook steps to tool calls or pseudo-actions
            - Provide structured resolution output (summary, steps, status)

            ## Acceptance Criteria
            - Example: IT password reset ticket flows through IT agent and returns steps
            - Runbook used is visible in logs or debug mode
        """).strip(),
        "labels": ["epic: agents", "priority: high", "type: backend"],
        "assignees": [ASSIGNEES["esthefany"], ASSIGNEES["portia"]],
    },
    {
        "title": "Implement HR agent logic with policy-aware responses",
        "body": dedent("""
            ## Summary
            HR agent should answer PTO/benefits/onboarding questions using synthetic policies.

            ## Tasks
            - Load HR policies (synthetic) from data or docs
            - Implement retrieval + reasoning pattern
            - Ensure responses are neutral and policy-aligned

            ## Acceptance Criteria
            - HR tickets resolve to clear answers citing HR policy snippets
        """).strip(),
        "labels": ["epic: agents", "priority: medium", "type: backend"],
        "assignees": [ASSIGNEES["nithya"]],
    },
    {
        "title": "Implement Finance agent logic for payroll/invoice tickets",
        "body": dedent("""
            ## Summary
            Finance agent handles payroll adjustments, reimbursements, and invoice/budget questions.

            ## Tasks
            - Define finance runbooks/workflows
            - Add simple rules around sensitive actions (no real banking data)
            - Ensure outputs are structured (amount, period, action_taken)

            ## Acceptance Criteria
            - Sample finance tickets resolve with a clear decision + justification
        """).strip(),
        "labels": ["epic: agents", "priority: medium", "type: backend"],
        "assignees": [ASSIGNEES["nithya"], ASSIGNEES["esthefany"]],
    },

    # EPIC 4 – Data & Synthetic Datasets
    {
        "title": "Curate IT synthetic tickets subset for demo",
        "body": dedent("""
            ## Summary
            Select a focused set of IT tickets for classifier training and demo.

            ## Tasks
            - Pull from HuggingFace IT helpdesk dataset (or existing data dir)
            - Tag a small, curated subset for the hackathon demo
            - Document which examples map to which runbooks

            ## Acceptance Criteria
            - `data/synthetic_tickets/it_demo.json` (or similar) exists
            - Each demo ticket has a known expected resolution path
        """).strip(),
        "labels": ["epic: data", "priority: medium", "type: data"],
        "assignees": [ASSIGNEES["megan"]],
    },
    {
        "title": "Curate HR & Finance synthetic tickets",
        "body": dedent("""
            ## Summary
            Prepare HR and Finance sample tickets for classifier + demo flows.

            ## Tasks
            - Select realistic HR and Finance tickets from Kaggle / synthetic generations
            - Make sure wording feels distinct across domains
            - Annotate expected domain + example resolution

            ## Acceptance Criteria
            - HR + Finance demo tickets stored under `data/`
            - At least 3–5 good demo tickets per domain
        """).strip(),
        "labels": ["epic: data", "priority: medium", "type: data"],
        "assignees": [ASSIGNEES["megan"], ASSIGNEES["nithya"]],
    },

    # EPIC 5 – Frontend / Demo Experience
    {
        "title": "Create simple ticket submission UI",
        "body": dedent("""
            ## Summary
            Build a small UI (web or Streamlit) to submit tickets and view resolutions.

            ## Tasks
            - Form for title, description, domain (optional), urgency
            - Call backend API
            - Display classification, agent, and final resolution

            ## Acceptance Criteria
            - Demo judges can submit a ticket live and see the system work
        """).strip(),
        "labels": ["epic: frontend", "priority: high", "type: frontend"],
        "assignees": [ASSIGNEES["portia"]],
    },
    {
        "title": "Add 'Agent reasoning' visualizer in UI",
        "body": dedent("""
            ## Summary
            Show a simplified 'reasoning trace' so judges see how TriResolve reached a decision.

            ## Tasks
            - Display domain classification result + confidence
            - Show which agent handled the ticket
            - Optionally list which runbook was executed

            ## Acceptance Criteria
            - UI clearly shows the steps the system took, not just the final answer
        """).strip(),
        "labels": ["epic: frontend", "priority: medium", "type: frontend"],
        "assignees": [ASSIGNEES["nithya"], ASSIGNEES["megan"]],
    },

    # EPIC 6 – Testing & Evaluation
    {
        "title": "Create minimal end-to-end test matrix",
        "body": dedent("""
            ## Summary
            Define and run a small E2E test matrix across IT, HR, and Finance tickets.

            ## Tasks
            - List 3–5 tickets per domain
            - Verify classification, agent selection, and resolution correctness
            - Capture any regressions or unexpected behaviors as separate issues

            ## Acceptance Criteria
            - E2E results documented in `docs/testing-summary.md`
            - Known gaps are tracked as issues
        """).strip(),
        "labels": ["epic: testing", "priority: high", "type: testing"],
        "assignees": [ASSIGNEES["nithya"], ASSIGNEES["megan"], ASSIGNEES["esthefany"]],
    },

    # EPIC 7 – Presentation & Story (Nithya + Megan)
    {
        "title": "Design TriResolve AI visual banner for Innovation Studio",
        "body": dedent("""
            ## Summary
            Create a banner/hero image that represents TriResolve AI for use in Innovation Studio and slides.

            ## Tasks
            - Choose color palette and visual style aligned with README
            - Export in required sizes (slide cover, banner, thumbnail)
            - Save in `docs/assets/`

            ## Acceptance Criteria
            - Banner file checked into repo
            - Used on first slide + any external listing (if allowed)
        """).strip(),
        "labels": ["epic: presentation", "priority: high", "type: design"],
        "assignees": [ASSIGNEES["nithya"]],
    },
    {
        "title": "Draft presentation slide outline (problem → solution → impact)",
        "body": dedent("""
            ## Summary
            Create the narrative flow for the final presentation.

            ## Tasks
            - Problem & pain points
            - Our approach (multi-agent, runbooks, synthetic data)
            - Demo flow
            - Business impact & future roadmap

            ## Acceptance Criteria
            - Slide outline captured in Notion or `docs/presentation-outline.md`
            - Team reviews and agrees on story arc
        """).strip(),
        "labels": ["epic: presentation", "priority: high", "type: documentation"],
        "assignees": [ASSIGNEES["portia"], ASSIGNEES["nithya"]],
    },
    {
        "title": "Build final presentation deck",
        "body": dedent("""
            ## Summary
            Turn the outline into a polished slide deck.

            ## Tasks
            - Apply TriResolve banner and visual theme
            - Add architecture + flow diagrams
            - Include 1–2 screenshots or mockups of the UI
            - Highlight what makes TriResolve different (tri-domain, runbooks, explainability)

            ## Acceptance Criteria
            - Slides stored in shared folder (and optionally linked in repo)
            - Ready for live presentation or recorded demo
        """).strip(),
        "labels": ["epic: presentation", "priority: high", "type: presentation"],
        "assignees": [ASSIGNEES["nithya"], ASSIGNEES["megan"]],
    },
    {
        "title": "Storyboard and rehearse demo flow",
        "body": dedent("""
            ## Summary
            Plan who says what, and in what order, during the live/recorded demo.

            ## Tasks
            - Decide which tickets to show
            - Script who speaks to which slides
            - Time the full run-through
            - Capture notes for improvement

            ## Acceptance Criteria
            - At least one full practice run completed
            - Demo fits inside required timebox
        """).strip(),
        "labels": ["epic: presentation", "priority: high", "type: presentation"],
        "assignees": [ASSIGNEES["nithya"], ASSIGNEES["megan"], ASSIGNEES["portia"]],
    },
]


# -----------------------------
# ISSUE CREATION LOGIC
# -----------------------------


def create_issue(issue):
    payload = {
        "title": issue["title"],
        "body": issue["body"],
        "labels": issue.get("labels", []),
        "assignees": issue.get("assignees", []),
    }
    resp = requests.post(API_URL, json=payload, headers=HEADERS)
    if resp.status_code == 201:
        url = resp.json().get("html_url")
        print(f"✅ Created: {issue['title']} -> {url}")
        return

    # If we receive a 422 validation error related to assignees, retry without assignees
    if resp.status_code == 422:
        has_assignee_error = False
        try:
            data = resp.json()
            errors = data.get("errors", [])
            for e in errors:
                # error entries may be dicts or strings depending on API response
                msg = e.get("message") if isinstance(e, dict) else str(e)
                if msg and "assignees" in msg:
                    has_assignee_error = True
                    break
        except Exception:
            has_assignee_error = "assignees" in resp.text

        if has_assignee_error and payload.get("assignees"):
            print(f"⚠️ Assignee validation failed for '{issue['title']}' — retrying without assignees...")
            payload.pop("assignees", None)
            resp2 = requests.post(API_URL, json=payload, headers=HEADERS)
            if resp2.status_code == 201:
                url = resp2.json().get("html_url")
                print(f"✅ Created (unassigned): {issue['title']} -> {url}")
                return
            else:
                print(f"❌ Retry Failed: {issue['title']}")
                print(f"Status: {resp2.status_code}")
                print(resp2.text)
                return

    # Fallback: print original error if not handled above
    print(f"❌ Failed: {issue['title']}")
    print(f"Status: {resp.status_code}")
    print(resp.text)


def main():
    print(f"Creating {len(ISSUES)} issues in {OWNER}/{REPO} ...")
    for issue in ISSUES:
        create_issue(issue)


if __name__ == "__main__":
    main()
