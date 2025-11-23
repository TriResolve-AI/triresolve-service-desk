# 🧠 TriResolve AI — Agent Architecture

This folder contains all agent logic, prompts, runbooks, and documentation that power **TriNexa**, the global orchestrator for the TriResolve AI multi-agent service desk.

---

## 🏗 Agent Architecture Diagram

Below is the conceptual topology showing how agents interact:

                         ┌────────────────────┐
                         │     TriNexa        │
                         │ (Global Router)    │
                         └─────────┬──────────┘
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
    ┌───────▼───────┐      ┌───────▼───────┐      ┌───────▼───────┐
    │      IT       │      │      HR       │      │    Finance    │
    │   Agent       │      │    Agent      │      │     Agent      │
    └──────┬────────┘      └──────┬────────┘      └──────┬────────┘
           │                      │                      │
           ▼                      ▼                      ▼
    Runbooks/Tools         Policies/Workflows     Approvals/Systems

---

## 🔗 How the Agents Fit Together

Each incoming ticket flows through the following pipeline:

1. **Intake Endpoint**  
   User submits a ticket via TriResolve UI.

2. **Classifier Model (Model 1)**  
   Predicts the domain: `IT`, `HR`, or `Finance`.

3. **TriNexa (Global Router)**  
   - Reads the predicted domain  
   - Maps to the correct agent  
   - Sends context + ticket metadata

4. **Domain Agent Executes**  
   - Loads the correct runbook  
   - Performs multi-step reasoning  
   - Returns structured output JSON

5. **TriNexa Combines Outputs**  
   - Adds meta-reasoning  
   - Format final response  
   - Sends result back to the user

---

## 📁 Folder Structure

The `/agents` folder is organized by domain:

agents/
├── it/
│ ├── it-agent.md
│ ├── runbooks/
│ ├── examples/
│ └── agent.py
│
├── hr/
│ ├── hr-agent.md
│ ├── runbooks/
│ ├── examples/
│ └── agent.py
│
├── finance/
│ ├── finance-agent.md
│ ├── runbooks/
│ ├── examples/
│ └── agent.py
│
└── docs/
├── classifier.md
├── architecture-diagram.md
└── reasoning-models.md


---

## 🧩 Agent Responsibilities

### **IT Agent**
- Hardware/software troubleshooting  
- Reset + access workflows  
- Device/network diagnostics  
- Software installs  
- MFA, password resets  

### **HR Agent**
- PTO, leave, benefits  
- Hiring & onboarding steps  
- Verification workflows  
- HR compliance  

### **Finance Agent**
- Payroll, reimbursements  
- Invoice approvals  
- Expense verification  
- Vendor workflows  

---

## 🧪 Testing the Agents

Use the `/scripts/run-agent.py` tool to simulate:

python scripts/run-agent.py --agent it --ticket "Reset my laptop password"

---

## 🧵 Reasoning Framework

All agents use a shared scaffold:

1. Extract intent  
2. Select runbook  
3. Execute step-by-step  
4. Produce structured JSON  
5. Return trace + explanation  

---

## 📚 Additional Docs

- `/agents/docs/classifier.md`  
- `/agents/docs/reasoning-models.md`  
- `/agents/docs/architecture-diagram.md`  

---

# ✔ This fixes your formatting issue

### Why your previous version broke:
- Markdown *requires a blank line before & after code blocks*
- Headings require a blank line before the next section
- GitHub collapses sections if lines run together
- Indented diagrams can accidentally “eat” all following text

This corrected version won’t collapse any sections.

---

