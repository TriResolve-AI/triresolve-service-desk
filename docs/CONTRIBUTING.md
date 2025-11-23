# 🧭 Contributing & Team Guide

Welcome to **TriResolve AI** — powered by our intelligent assistant **TriNexa**.

This guide outlines how our teams collaborate across repositories, how work is organized, and how to contribute effectively.

---

## 📌 Core Principles

- **Transparency:** All engineering, ML, UX, and documentation work runs through the shared project board.
- **Ownership:** Each team owns its domain but collaborates deeply with others.
- **Velocity > Perfection:** Small, iterative commits are preferred over large batches.
- **AI-augmented development:** Contributors are encouraged to use TriNexa + GitHub Copilot to speed up development.

---

## 🗺 Repository → Project → Team Mapping

| Layer / Component      | Name / Location                     | Who Uses It                         | Purpose |
|------------------------|--------------------------------------|--------------------------------------|---------|
| **GitHub Org**        | `TriResolve-AI`                      | Whole team                           | Central workspace containing all assets |
| **Main Repo**         | `triresolve-service-desk`            | Core Eng, AI/ML, Maintainers         | FastAPI backend, agents, workflows, API logic |
| **UI & Docs Repo**    | *(optional)* `triresolve-ux-assets`  | UX/UI + Docs                         | Slides, banners, UX workflows, documentation |
| **Data/ML Repo**      | *(optional)* `triresolve-ml-data`    | AI/ML                                | Synthetic data, classifier training, evaluation scripts |
| **Project Board**     | Org Project: `@TriResolve`           | All contributors                     | Centralized planning & task management |

---

## 📊 Project Board Structure

The board contains multiple work views to keep responsibilities clear:

- **Backlog** – all newly submitted ideas or tasks
- **Sprint 0** – environment setup, repo scaffolding
- **In Progress** – active work items
- **Review** – pending PR reviews, demo reviews
- **Done** – completed and approved
- **Team-focused Views**  
  - Core Engineering Items  
  - AI/ML Items  
  - UX/UI + Docs Items  
  - Priority Board (sorted by priority)  

---

## 👥 Team Responsibilities

### 🧩 **Core Engineering**
- Backend architecture (FastAPI)
- API design
- Agent routing infrastructure
- GitHub workflows / CI
- Environment setup & configurations

### 🧠 **AI/ML Agents**
- Ticket classifier model
- Agent policies & reasoning
- Synthetic data generation
- Execution + evaluation pipelines
- Research + algorithm improvements

### 🎨 **UX/UI + Documentation**
- System diagrams
- UI flows + microcopy
- Demo presentation & slides
- Visual assets / banners
- End-user documentation

### 🛡 Maintainers / Admin
- Repo permissions
- Label management
- Release approvals
- Final review & code quality

---

## 🧩 Contribution Workflow

### 1. Pick a Task  
Check the **@TriResolve** board under your team’s view.

### 2. Create a Branch  
Use a short naming pattern:

```
feature/<team>/<short-description>
fix/<team>/<short-description>
docs/<team>/<short-description>
```

### 3. Commit With Clear Messages  
Example:

```
feat(ai-agent): add initial policy routing logic
fix(core): correct env loading for FastAPI startup
docs(ux): add storyboard for demo flow
```

### 4. Open a Pull Request  
Include:
- What changed
- Why it matters
- Screenshots (if UI)
- Testing notes

### 5. Request Review  
Tag your team lead:
- Core Eng: `@portia`
- AI/ML: `@nithya`
- UX/UI: `@megan`
- Docs: `@estefany`

### 6. Merge Once Approved  
Maintainers handle final merges.

---

## 🌍 Meet TriNexa

TriResolve AI’s intelligent global assistant.

TriNexa helps:
- Generate code & workflows  
- Document architecture  
- Draft data schemas  
- Create UX flows & diagrams  
- Automate repetitive tasks  

Use TriNexa + GitHub Copilot at every stage for maximum speed.

---
