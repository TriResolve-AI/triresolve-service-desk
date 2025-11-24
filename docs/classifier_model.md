# 🧮 Classifier Model – Routing & Intent Guide

**File path:** `docs/classifier-model.md`

This document defines **Model 1 – the classifier** that routes incoming requests to the correct agent (IT, HR, Finance) or to other flows.

It is the source of truth for:
- Intent labels
- Routing rules
- Edge cases and fallbacks

---

## 1. Purpose

The classifier model is responsible for **deciding which agent (or system) should handle a request** before any in-depth reasoning happens.

Goals:
- Route tickets to the **correct agent** with high accuracy
- Keep the label set **simple and explainable**
- Provide clear guidance for ambiguous or multi-intent cases

---

## 2. Current Label Set

Base labels (can evolve over time):

- `IT` – Technology, access, devices, apps, connectivity
- `HR` – People, policies, time off, benefits
- `FINANCE` – Money, payments, reimbursements, invoices
- `UNKNOWN` – Not enough information to classify
- `OUT_OF_SCOPE` – Clearly not something the system should handle

### Example Mapping (Conceptual)

```json
{
  "IT": ["laptop", "computer", "password", "vpn", "email", "teams", "outlook", "wifi", "network"],
  "HR": ["pto", "vacation", "sick", "benefits", "health insurance", "onboarding", "offboarding", "policy"],
  "FINANCE": ["reimbursement", "expense report", "invoice", "payment", "payroll", "salary", "bonus", "cost center"],
  "UNKNOWN": [],
  "OUT_OF_SCOPE": []
}
```

The actual implementation should consider **semantics**, not just keywords, but this list acts as a **reference**.

---

## 3. Input & Output Format

### Input
- `message`: user’s natural language text
- Optional: metadata (user role, channel, language)

### Output (conceptual)

```json
{
  "label": "IT",
  "confidence": 0.87,
  "reasons": [
    "mentions password",
    "mentions login error",
    "common IT helpdesk scenario"
  ]
}
```

Implementation can be:
- Rule-based
- Embedding similarity
- LLM-based classification
- Or a hybrid approach

---

## 4. Routing Rules

1. If label = `IT` → Call **IT Agent**.
2. If label = `HR` → Call **HR Agent**.
3. If label = `FINANCE` → Call **Finance Agent**.
4. If label = `UNKNOWN` → Ask a **clarifying question** or route to a default agent (configurable).
5. If label = `OUT_OF_SCOPE` → Provide a polite message that it’s out of scope and optionally suggest next steps.

---

## 5. Handling Ambiguity & Multi-Intent

### Multi-domain Requests

If a message touches multiple domains (e.g., "I’m leaving the company, how does this affect my benefits and final paycheck?"), the classifier should:

- Choose the **primary** label based on context (e.g., `HR` for offboarding and benefits)
- Optionally pass along a **secondary label** as metadata (e.g., `FINANCE`), so the primary agent can address both or trigger a follow-up.

### Low Confidence

If confidence is below a threshold (e.g., `0.6`):

- Return `UNKNOWN`
- Add a reason such as "low confidence classification"
- Suggest asking a follow-up question before routing.

---

## 6. Fallbacks & Safety

The classifier should be biased toward:

- **Safety** – better to say "I’m not sure" than misroute a sensitive HR or Finance issue.
- **Simplicity** – a smaller label set is easier to maintain.

Examples of out-of-scope content:
- Personal legal advice
- Medical diagnoses
- Topics unrelated to workplace IT/HR/Finance

These should return `OUT_OF_SCOPE`.

---

## 7. Evaluation & Metrics

We can evaluate the classifier using:

- **Accuracy** – correct label vs human label
- **Confusion matrix** – common misroutes (e.g., HR vs Finance for payroll)
- **Coverage** – percentage of messages labeled as UNKNOWN

Target behavior:
- High accuracy for **common patterns**
- Limited UNKNOWNs, but not at the cost of bad guesses

---

## 8. Implementation Notes

- Configuration may live in `agents/classifier/intent_labels.json`.
- The orchestrator should log:
  - input text (anonymized)
  - predicted label
  - confidence
- Use those logs to refine labels and rules over time.

---

## 9. Future Extensions

- Add sub-labels (e.g., `IT_ACCESS`, `IT_DEVICE`, `HR_PTO`, `FIN_EXPENSE`)
- Add language detection and multilingual labels
- Plug into analytics dashboards for continuous improvement.

