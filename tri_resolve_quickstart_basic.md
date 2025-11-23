# 🚀 TriResolve AI – Quickstart Guide (Basic Version)

A fast, simple onboarding guide for contributors, teammates, and judges who need to understand **how to run or test TriResolve AI quickly**, without the deeper engineering details.

---

## ✅ What You Can Do With This Guide

This Quickstart helps you:

- Install the project
- Run the backend orchestrator
- Run the frontend UI
- Test all three agents (IT, HR, Finance)
- Understand the repo layout at a glance

If you need the advanced technical details, see the **Advanced Quickstart**.

---

# 📁 1. Repository Overview

```
triresolve-service-desk/
│
├── README.md
├── Quickstart.md              <- Basic guide (this file)
├── Quickstart-Advanced.md     <- Full detailed guide
├── agents/                    <- All agent prompts + docs
├── backend/                   <- Azure Functions + orchestrator
├── frontend/                  <- UI and workflow interface
└── docs/                      <- Architecture + diagrams
```

---

# 🧩 2. The Three Agents

TriResolve AI uses **three expert personas** to answer service desk requests:

### 👨‍💻 IT Agent

Handles issues like:

- Password reset
- Laptop problems
- VPN or network issues
- Software installation

### 🧑‍💼 HR Agent

Handles:

- PTO requests
- Benefits information
- Onboarding questions
- Policies & procedures

### 💰 Finance Agent

Handles:

- Reimbursements
- Invoices
- Payroll questions
- Cost center details

The system automatically decides **which agent** should answer.

---

# 🛠️ 3. Prerequisites

You only need:

- **Python 3.10+**
- **Node.js 18+**
- **Git**
- **VS Code** (optional but recommended)
- **Azure OpenAI API Key** (team lead provides this)

---

# 🖥️ 4. Install & Run the Backend (Fast Mode)

### 1️⃣ Clone the repo

```bash
git clone https://github.com/TriResolve-AI/triresolve-service-desk.git
cd triresolve-service-desk
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3️⃣ Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### 4️⃣ Create a `.env` file

Ask your team lead for the values.

```
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
```

### 5️⃣ Start the backend

```bash
cd backend/azure-functions
func start
```

If successful you’ll see:

```
http://localhost:7071/api/orchestrate
```

---

# 🌐 5. Run the Frontend

```bash
cd frontend/ui
npm install
npm run dev
```

The UI appears at:

```
http://localhost:5173
```

---

# 💬 6. Test the System (Basic Examples)

Use **curl**, Postman, or the built-in UI.

### IT Example

```bash
curl -X POST http://localhost:7071/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"message": "My laptop is slow"}'
```

### HR Example

```bash
-d '{"message": "How do I request PTO?"}'
```

### Finance Example

```bash
-d '{"message": "How do I submit a reimbursement?"}'
```

The system will return something like:

```json
{
  "agent": "HR",
  "response": "Here is how to request PTO..."
}
```

---

# 🔎 7. Where the Agent Prompts Live

```
agents/
  hr/prompts/HR_Agent_Prompts.md
  it/prompts/IT_Agent_Prompts.md
  finance/prompts/Finance_Agent_Prompts.md
```

Edit these if you want to adjust the agent’s personality, rules, or examples.

---

# 🤝 8. How to Contribute (Simple Rules)

1. **Create a new branch**

```bash
git checkout -b feature/my-update
```

2. **Commit your changes**

```bash
git commit -m "update: improved HR prompts"
```

3. **Push and create a Pull Request**

```bash
git push origin feature/my-update
```

4. Tag a reviewer.
5. Merge into `main` when approved.

---

# 🎉 9. You’re Ready!

This Basic Quickstart is enough to:

- Install
- Run
- Test
- Contribute
- Understand the core agents

The Advanced Quickstart provides deeper instructions for:

- Azure setup
- Architecture
- Deployment
- Classification models
- Security
- Reasoning scaffolds



