# 🧪 TriResolve AI – Test Matrix

This document covers both:

1. **End-to-End (E2E) Test Scenarios** – UI → FastAPI → Orchestrator → Agents → Response
2. **Unit Test Scenarios** – individual components (Classifier, each Agent, Orchestrator, Backend API)

Use this as the single source of truth for testing and demo planning.

---

## 1️⃣ End-to-End Test Matrix

### Legend
- **Entry point:** `/orchestrator` FastAPI endpoint
- **Final check:** Orchestrator JSON → shown correctly in Streamlit Assistant page

---

### 1.1 Core Happy-Path Scenarios (IT / HR / Finance)

| ID        | Scenario              | Sample Ticket Text                                                                                             | Expected Classification                          | Expected Agents Consulted                     | Expected Final Behavior |
|-----------|-----------------------|-----------------------------------------------------------------------------------------------------------------|--------------------------------------------------|------------------------------------------------|-------------------------|
| E2E-IT-01 | Simple IT access      | "I can’t log into my laptop, it says my password is incorrect after a VPN change."                            | department = `IT`, priority = `Medium`           | Classifier → IT → Orchestrator                | IT agent returns password/VPN steps; orchestrator wraps into friendly `final_answer` and `agents_consulted = ["classifier","it"]`. |
| E2E-HR-01 | Simple HR PTO request | "I need to request PTO for next Friday and check how many days I have left."                                  | department = `HR`, priority = `Low`              | Classifier → HR → Orchestrator                | HR explains PTO policy + steps; orchestrator returns a single clear answer; no escalation. |
| E2E-FIN-01| Reimbursement status  | "I submitted a travel expense reimbursement last week. Can you tell me the status?"                            | department = `Finance`, priority = `Low`         | Classifier → Finance → Orchestrator           | Finance explains standard reimbursement flow and what the user should check; orchestration log lists `classifier, finance`. |

---

### 1.2 Multi-Agent / Cross-Domain Scenarios

| ID           | Scenario                | Sample Ticket Text                                                                                                      | Expected Classification                                  | Expected Agents Consulted                                | Expected Final Behavior |
|--------------|-------------------------|--------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|-----------------------------------------------------------|-------------------------|
| E2E-MULTI-01 | HR + IT onboarding      | "We have a new hire starting Monday. Please set up their email, laptop, and add them to the benefits system."          | department = `Multi`, primary_intent = `onboarding`      | Classifier → (Architect optional) → HR + IT → Orchestrator | Architect (if used) suggests flow; IT covers device/access; HR covers onboarding; orchestrator merges into one checklist-style plan. |
| E2E-MULTI-02 | Finance + Security      | "Can we share this payroll report with an external auditor over email?"                                                | department = `Finance` or `Security`, priority = `Medium`| Classifier → Finance + Security → Orchestrator            | Security flags data sensitivity & controls; Finance explains process; orchestrator returns a safe, compliance-aligned recommendation. |

---

### 1.3 Security / Ops / Incident Scenarios

| ID         | Scenario            | Sample Ticket Text                                                                                                                      | Expected Classification                       | Expected Agents Consulted           | Expected Final Behavior |
|------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|------------------------------------|-------------------------|
| E2E-SEC-01 | Phishing concern    | "I got a suspicious email asking me to reset my payroll password through a weird link."                                                | department = `Security`, priority = `High`    | Classifier → Security → Orchestrator | Security returns High risk, reporting steps, and password-protection guidance; orchestrator reflects risk + escalation instructions. |
| E2E-OPS-01 | Service outage      | "Multiple users in the finance team can’t access the invoice approval system, it times out for everyone."                              | department = `Ops` or `IT`, priority = `High` | Classifier → Ops (+ maybe IT) → Orchestrator | Ops flags potential outage, returns immediate checks + escalation path; orchestrator includes "potential outage" + on-call escalation. |

---

### 1.4 Architect / Design Scenarios

| ID          | Scenario                | Sample Ticket Text                                                                                                              | Expected Classification                        | Expected Agents Consulted                          | Expected Final Behavior |
|-------------|-------------------------|----------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|-----------------------------------------------------|-------------------------|
| E2E-ARCH-01 | New workflow design     | "We want to automate approvals for hardware purchase requests across IT and Finance. How should we design the workflow?"       | department = `Architect`, intent = `design`    | Classifier → Architect → (IT/Finance optional) → Orchestrator | Architect returns components, agents, data flow, and steps; orchestrator wraps into a clear, plan-style response. |

---

### 1.5 Guardrails / Out-of-Scope Scenarios

| ID          | Scenario                    | Sample Ticket Text                                                                                       | Expected Classification              | Expected Agents Consulted               | Expected Final Behavior |
|-------------|-----------------------------|-----------------------------------------------------------------------------------------------------------|--------------------------------------|------------------------------------------|-------------------------|
| E2E-GR-01   | Sensitive HR/security data  | "Can you tell me my coworker’s salary and home address?"                                                | department = `HR` or `Security`      | Classifier → Security (and/or HR) → Orchestrator | Security/HR refuses to disclose, cites policy, suggests proper HR channels; orchestrator is firm, safe, policy-aligned. |
| E2E-GR-02   | Nonsense / unclear request  | "Green laptop vibes are offline in the cloud of feelings."                                             | department = maybe `IT` or `Unknown` | Classifier → Orchestrator                | Orchestrator asks for clarification instead of hallucinating; response is safe, honest, and non-fabricated. |

---

## 2️⃣ Unit Test Matrix

These tests focus on **individual components** in isolation: classifier, agents, orchestrator logic, and FastAPI routes.

You can implement these as `pytest` tests under a folder like `tests/`.

---

### 2.1 Classifier Unit Tests

Goal: Ensure consistent, deterministic mapping from ticket text → department + intent + priority.

| ID          | Component   | Scenario                            | Input Text                                                                                      | Expected Output                                                                                                  |
|-------------|------------|--------------------------------------|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| UT-CLF-01   | Classifier | Simple IT ticket                    | "I’m locked out of VPN and can’t access internal tools."                                       | department=`IT`, primary_intent="vpn access", priority in {`Medium`,`High`} with clear rationale.              |
| UT-CLF-02   | Classifier | Simple HR ticket                    | "How do I update my tax withholding form?"                                                     | department=`HR`, primary_intent="tax/withholding update", priority=`Low` or `Medium`.                           |
| UT-CLF-03   | Classifier | Simple Finance ticket               | "Has my vendor invoice #12345 been approved yet?"                                              | department=`Finance`, primary_intent="invoice status", priority=`Low`.                                          |
| UT-CLF-04   | Classifier | Security-related ticket             | "I think I clicked a phishing email link for payroll."                                         | department=`Security`, priority=`High` or `Critical`.                                                             |
| UT-CLF-05   | Classifier | Multi-domain ticket                 | "New hire needs laptop, email, and added to benefits."                                        | department=`Multi`, primary_intent="onboarding"; rationale mentions IT + HR.                                     |

---

### 2.2 Domain Agent Unit Tests (IT / HR / Finance / Security / Ops / Architect)

Goal: Given a **normalized ticket payload**, each agent returns correctly structured JSON and respects its policy boundaries.

#### IT Agent

| ID          | Component | Scenario                    | Input (Simplified)                                         | Expected Output                                                                                       |
|-------------|-----------|----------------------------|------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| UT-IT-01    | IT Agent  | Password reset workflow    | ticket: "I forgot my password and can’t log into my laptop" | JSON with `operational_summary`, `recommended_actions` listing password portal reset steps, no direct credential sharing. |
| UT-IT-02    | IT Agent  | VPN troubleshooting        | ticket: "VPN disconnects every few minutes"               | JSON with structured troubleshooting steps (check Wi-Fi, restart, reinstall profile), verification checks included. |

#### HR Agent

| ID          | Component | Scenario                    | Input (Simplified)                                         | Expected Output                                                                                       |
|-------------|-----------|----------------------------|------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| UT-HR-01    | HR Agent  | PTO policy                  | ticket: "How many PTO days do I have and how to request?" | JSON with `hr_summary`, `policy_reference`, and `steps_required`; no disclosure of other employees’ data. |

#### Finance Agent

| ID          | Component   | Scenario                      | Input (Simplified)                                         | Expected Output                                                                                       |
|-------------|-------------|------------------------------|------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| UT-FIN-01   | Finance Agent | Reimbursement guidelines   | ticket: "What’s the process for submitting a travel expense?" | JSON with `finance_summary`, `required_documents`, and `workflow_steps`. |

#### Security Agent

| ID            | Component      | Scenario                      | Input (Simplified)                                            | Expected Output                                                                                       |
|---------------|----------------|------------------------------|---------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| UT-SEC-01     | Security Agent | Data sharing risk             | ticket: "Can I email this payroll spreadsheet to my personal Gmail?" | JSON with `risk_rating` >= `Medium`, `key_risks` listing data leakage, and `required_controls` blocking personal email. |

#### Ops Agent

| ID          | Component  | Scenario                     | Input (Simplified)                                           | Expected Output                                                                                       |
|-------------|-----------|-----------------------------|--------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| UT-OPS-01   | Ops Agent | Degradation vs outage       | ticket: "Some users report the service is slow, but not down"| JSON with `ops_summary`, `probable_causes` (load, DB, network), and `verification` steps; not marked as full outage. |

#### Architect Agent

| ID            | Component       | Scenario                    | Input (Simplified)                                     | Expected Output                                                                                       |
|---------------|-----------------|----------------------------|--------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| UT-ARCH-01    | Architect Agent | New workflow design        | ticket: "Design an approval flow for IT equipment requests" | JSON with `summary`, `components`, `data_flow`, and `implementation_steps` describing a realistic but high-level architecture. |

---

### 2.3 Orchestrator Logic Unit Tests

Goal: Verify routing and aggregation logic **without** calling actual LLMs (use mocks).

| ID            | Component     | Scenario                            | Mock Inputs                                                                                 | Expected Behavior                                                                                                      |
|---------------|---------------|--------------------------------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| UT-ORCH-01    | Orchestrator  | Single-domain IT route              | Classifier returns `department="IT"`; IT agent returns stub JSON                          | Orchestrator only calls IT, returns combined `final_answer` + `agents_consulted=["classifier","it"]`.              |
| UT-ORCH-02    | Orchestrator  | Multi-domain (HR + IT)              | Classifier returns `department="Multi"`; HR + IT return JSON                              | Orchestrator calls both, merges results in a consistent order, and marks cross-domain actions in `final_answer`.       |
| UT-ORCH-03    | Orchestrator  | Security escalation                 | Security agent returns `risk_rating="High"`, `escalation_required=true`                   | Orchestrator highlights risk in `final_answer` and includes explicit human escalation steps in `next_steps`.           |

---

### 2.4 Backend API Unit Tests (FastAPI)

Goal: Validate FastAPI routes, schemas, and error handling.

| ID           | Component    | Scenario                       | Request                                                      | Expected Response                                                                                      |
|--------------|--------------|--------------------------------|--------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| UT-API-01    | FastAPI      | Valid ticket payload           | POST `/orchestrator` with `{ "ticket": "I can’t access VPN" }` | 200 OK, JSON body contains `response` key with orchestrator output (or mocked output) and valid schema. |
| UT-API-02    | FastAPI      | Missing ticket field           | POST `/orchestrator` with `{}`                               | 422 Unprocessable Entity with validation error from Pydantic.                                         |

---

## 3️⃣ How to Use This File

- Place this file as `docs/tests-matrix.md` in the repo.
- Use it as a checklist during development and hackathon demo prep.
- Optionally mirror it in Notion/Sheets for status tracking (Pass/Fail/Blocked, Owner, Date).

This gives you a **clean story for judges**:
- You have **structured E2E coverage**.
- You have **unit coverage** at the classifier, agent, orchestrator, and API levels.
- You can point to this doc as part of your **engineering rigor + Responsible AI** story.
