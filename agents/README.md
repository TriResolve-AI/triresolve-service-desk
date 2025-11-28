# 🧠 TriResolve AI — Agent Architecture

This folder contains all agent logic, prompts, runbooks, examples, and documentation that power **TriResolve AI** and **TriNexa**, the global multi-agent orchestrator for the service desk.

Agents are created and managed in **Azure AI Foundry** and invoked from the backend via **Azure OpenAI**.

---

## 🏗 Agent Topology

High-level view of how everything fits together:

                         ┌───────────────────────────┐
                         │        TriNexa            │
                         │  (Global Orchestrator)    │
                         └────────────┬──────────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
      ┌──────▼───────┐        ┌───────▼───────┐        ┌───────▼───────┐
      │ Classifier   │        │  Architect    │        │   Security    │
      │  Agent       │        │   Agent       │        │    Agent      │
      └──────┬───────┘        └──────┬───────┘        └──────┬────────┘
             │                        │                        │
             ▼                        ▼                        ▼
      Ticket domain &         System / solution         Risk, policy &
      intent routing          design & planning         compliance review

             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
      ┌──────▼───────┐        ┌───────▼───────┐        ┌───────▼───────┐
      │     IT       │        │      HR       │        │    Finance    │
      │    Agent     │        │    Agent      │        │     Agent     │
      └──────┬───────┘        └──────┬───────┘        └──────┬────────┘
             │                        │                        │
             ▼                        ▼                        ▼
   IT tickets & tools        People / policy / HR       Payments, vendors,
                             workflows                  budgets, approvals

                          ┌──────────────────────┐
                          │        Ops           │
                          │       Agent          │
                          └─────────┬────────────┘
                                    ▼
                          Incidents, SLO/SLA,
                          logs, reliability

---

## 🔗 End-to-End Flow

1. **Ticket Intake**  
   A ticket is submitted via the TriResolve UI or API and sent to the backend.

2. **Classification**  
   The backend calls the **Classifier Agent**, which predicts:
   - Domain: `IT`, `HR`, `Finance`, `Security`, `Ops`, or `Architect`
   - Priority and intent (where supported)

3. **Orchestration via TriNexa**  
   The **TriNexa Orchestrator Agent**:
   - Reads the classification and ticket details  
   - Decides which agents to call (one or many)  
   - Aggregates and reconciles their responses  

4. **Domain Agent Execution**  
   Each domain agent:
   - Applies its persona + policies  
   - May use tools/knowledge bases (runbooks, docs, KBs)  
   - Returns a structured result (JSON-like fields: summary, steps, risk, etc.)

5. **Final Answer**  
   TriNexa returns a **single, user-friendly response** back to the backend, which is sent to the UI.

---

## 📁 Folder Structure

The `/agents` folder is organized by agent domain, with a consistent pattern:

```text
agents/
├── docs/
│   ├── agents-architecture.md
│   ├── classifier.md
│   └── orchestration-model.md
│
├── classifier/
│   ├── agent.py
│   ├── agent.md        # Foundry instructions / persona
│   └── examples/
│
├── orchestrator/
│   ├── agent.py
│   ├── agent.md
│   └── runbooks/
│
├── it/
│   ├── agent.py
│   ├── agent.md
│   ├── runbooks/
│   └── examples/
│
├── hr/
│   ├── agent.py
│   ├── agent.md
│   ├── runbooks/
│   └── examples/
│
├── finance/
│   ├── agent.py
│   ├── agent.md
│   ├── runbooks/
│   └── examples/
│
├── architect/
│   ├── agent.py
│   ├── agent.md
│   └── examples/
│
├── security/
│   ├── agent.py
│   ├── agent.md
│   └── runbooks/
│
└── ops/
    ├── agent.py
    ├── agent.md
    └── runbooks/
