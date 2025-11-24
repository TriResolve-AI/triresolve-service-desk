# 🧾 Prompt Templates – Conventions & Structure

**File path:** `docs/prompt-templates.md` (suggested)

This document defines how we design and organize **prompt templates** for all agents in TriResolve AI / TriNexa.

It complements the per-agent prompt files under:

```text
agents/hr/prompts/HR_Agent_Prompts.md
agents/it/prompts/IT_Agent_Prompts.md
agents/finance/prompts/Finance_Agent_Prompts.md
```

---

## 1. Goals

Our prompt templates should:

- Be **consistent** across agents
- Make it easy for contributors to update behavior safely
- Separate **persona**, **reasoning**, and **tools**
- Be readable by non-engineers (e.g., judges, PMs, HR/IT/Finance partners)

---

## 2. Standard Prompt Sections

Each agent prompt file should follow this structure (sections can be adapted per agent):

1. **Overview**
   - Short description of the agent and its domain.

2. **System Instruction / Role**
   - One or two paragraphs describing who the agent is, what it can and cannot do.

3. **Tone & Style Guidelines**
   - Bullet list of voice/tone rules.

4. **Reasoning Framework (Condensed)**
   - Short version of the reasoning steps from `docs/reasoning-framework.md`.

5. **Tools & Capabilities**
   - What integrations or runbooks the agent may call.

6. **Safety & Escalation**
   - When to defer to a human or label something as out-of-scope.

7. **Input & Output Expectations**
   - Expected fields and any JSON structure if used.

8. **Examples**
   - A few sample Q&A or conversation snippets, including edge cases.

---

## 3. Example Skeleton – HR Agent Prompt File

**File:** `agents/hr/prompts/HR_Agent_Prompts.md`

```md
# HR Agent – Prompt Template

## 1. Overview
You are the HR Agent for TriResolve AI / TriNexa. You assist employees and managers with HR-related questions, following company policies and escalating sensitive issues.

## 2. System Instruction / Role
- You specialize in HR topics: PTO, benefits, onboarding, policies, etc.
- You always stay neutral and respectful.
- You do not give legal advice or make binding promises.

## 3. Tone & Style
- Warm, supportive, and clear.
- Use plain language and avoid heavy jargon.
- Use short paragraphs and bullet points for clarity.

## 4. Reasoning Framework (Condensed)
When you respond, internally follow these steps:
1. Understand and summarize the user’s question.
2. Classify the topic (PTO, benefits, onboarding, etc.).
3. Check for sensitive issues (harassment, discrimination, medical, legal risk).
4. Select the correct policy or runbook.
5. Provide a clear, structured answer with steps.
6. Recommend escalation when appropriate.

## 5. Tools & Capabilities
You can:
- Reference HR runbooks (e.g., PTO process, onboarding checklist).
- Provide links or instructions for HR systems.
You cannot:
- Access or change employee records directly.

## 6. Safety & Escalation
Escalate when:
- The issue involves harassment, discrimination, or serious conflict.
- The user requests exceptions to policy.

## 7. Input & Output Expectations
Input: User’s question in natural language.
Output: A helpful answer in markdown with:
- Short intro sentence.
- Steps or bullets.
- Suggestions for next actions.

## 8. Examples
**User:** "How do I request PTO?"
**You:** (Provide a clear, step-by-step answer.)
```

Use a similar skeleton for IT and Finance agents.

---

## 4. Naming Conventions

- Use **Title_Case_Agent_Prompts.md** for agent-level prompt files:
  - `HR_Agent_Prompts.md`
  - `IT_Agent_Prompts.md`
  - `Finance_Agent_Prompts.md`

- For specialized prompt sets (optional):
  - `HR_Onboarding_Prompts.md`
  - `IT_Incident_Prompts.md`

---

## 5. Editing Guidelines

When editing prompt templates:

1. Keep changes **scoped** to one agent at a time.
2. Avoid hard-coding specific people, dates, or confidential details.
3. Document behavioral changes briefly at the top or in the PR description.
4. Keep examples **generic but realistic**.

---

## 6. Review Checklist

Before merging changes to a prompt file, verify:

- [ ] Does the prompt still match the persona doc in `docs/agents/<agent>-agent.md`?
- [ ] Are safety and escalation rules clearly stated?
- [ ] Are reasoning steps included in a compact form?
- [ ] Are examples correct and free of sensitive data?

---

## 7. Future Enhancements

- Add language-specific prompt variants (multi-lingual support).
- Create prompt snippets for common patterns (clarifying questions, disclaimers, etc.).
- Link prompts directly to **evaluation scenarios** for testing.

This document should remain the central reference for **how we design prompts** across agents.

