# TriResolve AI Hackathon Milestones

This document outlines the key milestones for the TriResolve AI project.

## Project Milestones

### M1 – Foundations Ready
**Description:** Core repository setup, tooling, and documentation foundations are in place.

**Key Deliverables:**
- Repository structure established
- CONTRIBUTING.md finalized
- Basic CI/CD workflows configured
- Team collaboration tools set up

---

### M2 – Backend Routing + Agents
**Description:** Backend API is functional with agent routing and domain classification.

**Key Deliverables:**
- FastAPI backend operational
- Agent router implemented
- IT/HR/Finance agent entrypoints defined
- Basic error handling in place

---

### M3 – Classifier + API
**Description:** Domain classifier is trained/integrated and API endpoints are complete.

**Key Deliverables:**
- Domain classifier model integrated
- Classification accuracy validated
- All API endpoints functional
- Request/response validation implemented

---

### M4 – Demo UX & Storyboard
**Description:** Demo UI and presentation storyboard are ready for rehearsal.

**Key Deliverables:**
- Ticket submission UI complete
- Agent reasoning visualizer working
- Demo flow documented
- Presentation outline created

---

### M5 – Full System Demo
**Description:** End-to-end system demonstration is working and rehearsed.

**Key Deliverables:**
- End-to-end ticket resolution flow tested
- Demo rehearsal completed
- Known issues documented
- Fallback scenarios prepared

---

### M6 – Final Submission
**Description:** All deliverables complete and submitted for hackathon judging.

**Key Deliverables:**
- Presentation deck finalized
- All code merged and tested
- Documentation complete
- Project submitted for evaluation

---

## Creating Milestones in GitHub

To create these milestones in the GitHub repository, run:

```bash
export GITHUB_TOKEN="your_github_token"
python3 scripts/create_milestones.py
```

This will create all six milestones via the GitHub API. Once created, you can assign issues to these milestones through the GitHub UI or API.

---

## Milestone Timeline

The milestones are designed to be completed sequentially, with each building on the previous:

1. **M1** → Foundation and setup
2. **M2** → Backend and core logic
3. **M3** → AI/ML integration
4. **M4** → User experience and presentation
5. **M5** → Integration and rehearsal
6. **M6** → Final polish and submission
