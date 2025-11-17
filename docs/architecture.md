#  TriResolve AI  Architecture Overview

TriResolve AI is a **multiagent service desk orchestrator** designed to automatically resolve **IT, HR, and Finance support tickets** using  
**Azure AI Foundry Agents**, **retrievalaugmented runbooks**, and **synthetic ticket datasets**.

The goal is to demonstrate intelligent triage, domain classification, automated actions, and clean endtoend resolution within a hackathon timeframe.

---

#  System Components

## 1.  FastAPI Backend  
The backend acts as the **central orchestration hub**.

### **Responsibilities**
-  Receives & validates incoming tickets (API or UI)  
-  Classifies the ticket domain (**IT / HR / Finance**)  
-  Routes tasks to the appropriate agent  
-  Executes YAMLbased runbook steps  
-  Returns structured resolutions to the user  

---

## 2.  Agent Layer (Azure AI Foundry MultiAgents)

Each agent includes:
-  Domainspecific reasoning  
-  Internal YAML runbooks  
-  Python toolcalling for automated steps  
-  Retrieval of relevant policies, SOPs, and references  

###  IT Agent
Handles common IT helpdesk tasks:
-  Password resets  
-  VPN access issues  
-  Account lockouts  
-  Device troubleshooting  

###  HR Agent
Handles HRrelated workflows:
-  PTO requests  
-  Benefits questions  
-  Policy lookup  
-  Onboarding support  

###  Finance Agent
Handles financial processes:
-  Payroll adjustments  
-  Reimbursements  
-  Invoice or budget queries  

---

## 3.  Runbooks (YAMLBased Automation)

Runbooks define **consistent, repeatable procedures** for agents to execute.

###  Example  IT Password Reset
```yaml
action: password_reset
steps:
  - validate_user_identity
  - check_AD_lockout_status
  - reset_password
  - notify_user: "Your password has been reset."
```

Runbooks ensure **predictable, safe automation** for the hackathon demo.

---

## 4.  Synthetic Datasets

Synthetic datasets simulate realistic ticket flows for all domains.

### Used for:
-  Training the domain classifier  
-  Generating agent prompt examples  
-  Testing endtoend resolution scenarios  

### Sources:
-  IT Helpdesk synthetic tickets (HuggingFace)  
-  HR datasets (Kaggle)  
-  Finance datasets (Kaggle)  

---

#  HighLevel Ticket Resolution Flow

```text
User  FastAPI Backend  Classifier  Agent (IT / HR / Finance)
       Runbook Execution  Final Resolution  User
```

---

#  Expanded StepByStep Flow

### **1. User submits a ticket**
May come from:
- Web form  
- Mobile app  
- Internal portal  
- API request  

### **2. Backend receives & parses request**
- Extracts metadata  
- Validates ticket structure  

### **3. Classifier determines the domain**
Trained on synthetic datasets for:
- IT  
- HR  
- Finance  

### **4. Backend activates correct agent**
Agent options:
-  IT Agent  
-  HR Agent  
-  Finance Agent  

### **5. Agent executes workflow**
Includes:
- Interpreting ticket text  
- Retrieving relevant policies/runbooks  
- Executing YAML runbook steps  
- Calling Python tools if needed  

### **6. Backend returns structured resolution**
Includes:
-  Resolution text  
-  Steps taken  
-  Confidence score  
-  Any recommended followups  

User receives **complete, automated resolution**.

---

#  Project Directory Structure

```text
backend/
  main.py
  api/
    routes.py
  agents/
    it_agent.py
    hr_agent.py
    finance_agent.py

runbooks/
  it/
  hr/
  finance/

docs/
  architecture.md

requirements.txt
Dockerfile
```

---

#  Hackathon Deployment Model

-  FastAPI backend is containerized for portability  
-  Agents run locally in a simulated Azure Foundry setup  
-  Runbooks stored as YAML for rapid iteration  
-  Synthetic data is injected during build  
-  Optimized for **fast judging and demo presentations**  

---

#  Hackathon Objectives

TriResolve AI aims to deliver:
-  A functional multiagent autoresolution system  
-  Accurate domain classification  
-  Deterministic runbook execution  
-  Clear logs & explainability  
-  Reliable endtoend resolution demo  

This architecture is optimized for **rapid development within a 2week hackathon**, while providing a foundation for future expansion.

---
