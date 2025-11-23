# 🚀 TriResolve AI – Advanced Quickstart Guide
_For the TriResolve AI Service Desk Orchestrator_

This guide gives you everything you need to install, run, and extend the TriResolve Service Desk Orchestrator — including local setup, Azure resources, multi-agent execution, repo structure, and development workflows.

> **Audience:** Developers, engineers, and hackathon contributors who need a fast but complete onboarding experience.

---

## 📁 1. Repository Structure Overview

```text
triresolve-service-desk/
│
├── README.md
├── Quickstart.md        <- you are here
├── CONTRIBUTING.md
│
├── agents/
│   ├── hr/
│   │   ├── prompts/
│   │   │   └── HR_Agent_Prompts.md
│   │   └── docs/
│   │       └── HR_Runbooks.md
│   ├── it/
│   │   ├── prompts/
│   │   │   └── IT_Agent_Prompts.md
│   │   └── docs/
│   ├── finance/
│   │   ├── prompts/
│   │   │   └── Finance_Agent_Prompts.md
│   │   └── docs/
│   └── classifier/
│       └── intent_labels.json
│
├── backend/
│   ├── orchestrator/
│   ├── azure-functions/
│   └── semantic-kernel/
│
├── frontend/
│   ├── ui/
│   └── workflows/
│
└── docs/
    └── architecture/
```

---

## 🛠️ 2. Prerequisites

### Required
- Python 3.10+
- Node.js 18+
- Azure CLI
- Azure Subscription
- Azure OpenAI resource (GPT-4 class model)
- Azure Functions Core Tools
- Git + GitHub access
- VS Code (recommended) with:
  - Azure Tools
  - Python
  - GitHub Copilot (optional but helpful)

---

## ☁️ 3. Azure Resources You Will Need

Create these once per team:

| Resource | Purpose |
|---------|---------|
| Azure OpenAI | LLM for agent prompts and orchestration |
| Azure Function App | Agent execution and workflow logic |
| Azure Blob Storage | Knowledge/docs upload and retrieval |
| Azure AI Search (optional) | Structured HR/IT/Finance retrieval |
| Cosmos DB (optional) | Persistent state, ticket data |
| Static Web App | Front-end UI |

Example: create core resource group and OpenAI:

```bash
az group create -n triresolve-rg -l eastus

az cognitiveservices account create \  
  -n triresolve-openai \  
  -g triresolve-rg \  
  --kind OpenAI \  
  --sku s0 \  
  --location eastus
```

---

## 📦 4. Local Installation (Backend)

Clone the repo:

```bash
git clone https://github.com/TriResolve-AI/triresolve-service-desk.git
cd triresolve-service-desk
```

Create a Python environment:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Create a `.env` file in the repo root:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=triresolve-gpt
BLOB_CONNECTION_STRING=
AI_SEARCH_ENDPOINT=
AI_SEARCH_KEY=
COSMOS_URI=
COSMOS_KEY=
```

---

## 🧠 5. Understanding the Multi-Agent System

TriResolve uses three expert personas, each with its own:

- System prompt
- Reasoning scaffold
- Allowed actions
- Runbook library
- Example output formats
- Escalation rules

### Agents

- **IT Agent** – Technical issues, access, devices, troubleshooting
- **HR Agent** – PTO, benefits, onboarding, policy
- **Finance Agent** – Reimbursements, invoices, payroll, cost centers

### Classifier Model (Model 1)

Before any agent runs, a lightweight classifier identifies the correct agent.

Example `intent_labels.json`:

```json
{
  "IT": ["laptop", "vpn", "software", "outage", "password"],
  "HR": ["pto", "benefits", "onboarding", "policy"],
  "FINANCE": ["reimbursement", "invoice", "payment", "payroll"]
}
```

---

## 🏃 6. Running the System Locally

Start the Azure Function orchestrator:

```bash
cd backend/azure-functions
func start
```

You should see an endpoint like:

```text
http://localhost:7071/api/orchestrate
```

Send a test payload:

```bash
curl -X POST http://localhost:7071/api/orchestrate \  
  -H "Content-Type: application/json" \  
  -d '{"message": "I need to reset my password"}'
```

Expected response (shape will vary):

```json
{
  "agent": "IT",
  "action": "walkthrough",
  "response": "Here is how to reset your password..."
}
```

---

## 🎨 7. Front-End Setup

From the repo root:

```bash
cd frontend/ui
npm install
npm run dev
```

By default:

```text
http://localhost:5173
```

Front-end environment variables live under:

```text
frontend/.env
```

---

## 🧩 8. Adding or Modifying Agent Prompts

Each agent has a dedicated prompt file:

```text
agents/hr/prompts/HR_Agent_Prompts.md
agents/it/prompts/IT_Agent_Prompts.md
agents/finance/prompts/Finance_Agent_Prompts.md
```

Each file should contain:

1. System instruction
2. Style and tone
3. Reasoning / steps-of-thinking scaffold
4. Tools available
5. Escalation rules
6. Example interactions
7. Output JSON schema

To update prompts:

1. Edit the `.md` file.
2. Create a feature branch:
   ```bash
   git checkout -b agent/hr-updates
   ```
3. Commit and push:
   ```bash
   git commit -m "chore: refine HR agent prompts"
   git push origin agent/hr-updates
   ```
4. Open a pull request to `main`.

---

## 📚 9. Adding New Runbooks

Runbooks live under:

```text
agents/<agent>/docs/
```

Examples:

```text
agents/hr/docs/HR_Runbooks.md
agents/it/docs/IT_Troubleshooting.md
agents/finance/docs/Finance_Policy.md
```

When adding a new runbook:

- Add it to the appropriate `docs/` folder.
- Link it from the agent’s prompt file where relevant.
- Ensure the orchestrator can reference it if the agent needs structured access.

---

## 🧪 10. Testing the Full Orchestration Flow

You can simulate agent traffic via the orchestrator API.

### IT Example

```bash
curl -X POST http://localhost:7071/api/orchestrate \  
  -H "Content-Type: application/json" \  
  -d '{"message": "Teams is not working on my laptop"}'
```

### HR Example

```bash
curl -X POST http://localhost:7071/api/orchestrate \  
  -H "Content-Type: application/json" \  
  -d '{"message": "How do I request PTO?"}'
```

### Finance Example

```bash
curl -X POST http://localhost:7071/api/orchestrate \  
  -H "Content-Type: application/json" \  
  -d '{"message": "I need to submit a reimbursement"}'
```

---

## 🚀 11. Deployment Workflow

### 1. Push to GitHub

Push your changes to a branch on GitHub. Optionally, GitHub Actions can build and test.

### 2. Deploy Azure Functions

```bash
func azure functionapp publish triresolve-functions
```

### 3. Deploy Front-End

Using Azure Static Web Apps (example):

```bash
az staticwebapp create \  
  --name triresolve-ui \  
  --resource-group triresolve-rg \  
  --source .
```

Configure build settings in the portal or via workflow as needed.

---

## 🔒 12. Security Model

- No PII stored in source-controlled config.
- Use Azure Key Vault or environment variables for secrets.
- Role-based agent access enforced in the orchestrator.
- Prompt templates contain no sensitive customer data.
- Logs should be anonymized and scrubbed before sharing.

---

## 🤝 13. Contributing Workflow

1. Create a new branch:

   ```bash
   git checkout -b feature/<name>
   ```

2. Commit changes:

   ```bash
   git commit -m "feat: added new IT runbook"
   ```

3. Push and open a PR:

   ```bash
   git push origin feature/<name>
   ```

4. Tag reviewers and iterate until approved.
5. Merge into `main`.

See `CONTRIBUTING.md` for more details.

---

## 🎯 14. Glossary of Terms

| Term | Meaning |
|------|---------|
| Orchestrator | Core logic that routes tasks to agents |
| Agent | A specialized persona with its own prompt and rules |
| Classifier | Lightweight model that picks the correct agent |
| Runbook | Standard procedure followed by the agent |
| Tool | API/action an agent can invoke |
| Escalation | Hand-off to human or a different agent |

---

## 🧵 15. Roadmap (Hackathon Priorities)

- Agent prompt templates
- Steps-of-reasoning scaffolds
- Classification label set
- Runbook library
- UI integration
- End-to-end test harness
- Final architecture diagram
- Final pitch deck

---

## 🎉 You're Ready

This Advanced Quickstart is designed so contributors, mentors, and judges can quickly understand and run the TriResolve Service Desk Orchestrator.

If you need a lighter-weight version, you can create a `Quickstart-Basic.md` that links here for deeper details.

