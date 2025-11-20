# 🏗 Architecture Overview

TriResolve AI is built using a layered, modular, agent-driven architecture.

## Contents

- [High-Level Architecture](#-high-level-architecture)
- [Core Components](#-core-components)
- [Planned Enhancements](#-planned-architecture-enhancements)

---

## 🔹 High-Level Architecture

User → Service Desk Portal → API Gateway (FastAPI)

TriNexa (Global Coordinator)

┌─────────────┬──────────────┬─────────────┐
| IT Agent    | HR Agent     | Finance     |
| Troubleshoot| HR policies  | Approvals   |
| Automations | Compliance    | Invoices    |
└─────────────┴──────────────┴─────────────┘

---

## 🔹 Core Components

### **1. API Gateway (FastAPI)**

- Unified entry point
- Request validation
- Dispatches to TriNexa

### **2. TriNexa — Global AI Assistant**

- Primary orchestrator
- Tickets → classification → agent routing
- Manages complex multi-hop reasoning
- Coordinates between IT, HR, Finance workflows

### **3. Domain Agents**

- **IT Agent:** troubleshooting, device setups, password resets
- **HR Agent:** onboarding, policy questions, verifications
- **Finance Agent:** payroll, vendor queries, approvals

### **4. Data Layer**

- Synthetic datasets
- Realistic patterns for org requests
- ML models trained on diverse scenarios

---

## 📦 Planned Architecture Enhancements

- Real-time event bus
- Memory store for agent context
- Vector search for long-term reasoning

