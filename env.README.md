# 🔐 TriResolve AI – Environment & Secrets Guide

This document explains all required environment variables for the **TriResolve AI / TriNexa** project and where they should be configured.

> ⚠️ Never commit real secrets or `.env` files to the repository.  
> Use `.env.example` as a template only.

---

## 📁 Files & Places Where Env Vars Are Used

| Location                  | Purpose                                   | Contains real secrets? |
|---------------------------|-------------------------------------------|-------------------------|
| `.env.example`            | Template for required variables           | ❌ Never                |
| `.env` (local, ignored)   | Your local dev configuration              | ✅ Yes                  |
| GitHub → Repo Secrets     | CI/CD & automation configuration          | ✅ Yes                  |
| Streamlit Cloud Secrets   | Deployed Streamlit app configuration      | ✅ Yes                  |

---

## 🔧 Core Azure Settings

### `AZURE_OPENAI_ENDPOINT`

- **What it is:**  
  Base URL for your Azure OpenAI / Azure AI Foundry resource.  
- **Example:**  
  `https://your-resource.openai.azure.com`
- **Where to set it:**  
  - `.env`
  - GitHub Repo Secrets
  - Streamlit Secrets (if Streamlit calls Azure directly)

---

### `AZURE_OPENAI_API_KEY`

- **What it is:**  
  Primary API key for your Azure OpenAI / Foundry resource.
- **Important:**  
  Treat this like a password. Never share or commit it.
- **Where to set it:**  
  - `.env`
  - GitHub Repo Secrets
  - Streamlit Secrets (if needed)

---

### `AZURE_LOCATION`

- **What it is:**  
  Azure region where your resource is deployed.
- **Example:**  
  `eastus`
- **Why it matters:**  
  Some SDKs and tools require the region explicitly for routing, logging, or resource discovery.
- **Where to set it:**  
  - `.env`
  - GitHub Repo Secrets
  - (Optional) Streamlit Secrets

---

## 🧠 Agent Deployment Variables

These map **logical agent roles** (HR, IT, Finance, Architect, etc.) to the **actual deployment names** in Azure AI Foundry.

> The values must match the model/agent names shown in the Foundry "Code" tab.

### `AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR`

- **Role:** Central orchestrator that coordinates classifier + domain agents.
- **Example value:** `triresolve-orchestrator`
- **Used by:** Backend orchestrator client.

---

### `AZURE_OPENAI_DEPLOYMENT_CLASSIFIER`

- **Role:** Intent router that classifies incoming tickets (HR vs IT vs Finance, etc.).
- **Example value:** `triresolve-classifier`
- **Used by:** Orchestrator / routing logic.

---

### `AZURE_OPENAI_DEPLOYMENT_HR`

- **Role:** HR domain specialist – onboarding, PTO, benefits, etc.
- **Example value:** `triresolve-hr`

### `AZURE_OPENAI_DEPLOYMENT_IT`

- **Role:** IT service desk specialist – VPN, laptop, access requests, etc.
- **Example value:** `triresolve-it`

### `AZURE_OPENAI_DEPLOYMENT_FINANCE`

- **Role:** Finance specialist – invoices, reimbursements, vendor setup, etc.
- **Example value:** `triresolve-finance`

---

### `AZURE_OPENAI_DEPLOYMENT_ARCHITECT`

- **Role:** System design / architecture advisor (TriNexa Architect Agent).
- **Example value:** `triresolve-architect`

### `AZURE_OPENAI_DEPLOYMENT_SECURITY`

- **Role:** Security & governance advisor (TriNexa Security Agent).
- **Example value:** `triresolve-security`

### `AZURE_OPENAI_DEPLOYMENT_OPS`

- **Role:** Operations / observability advisor (TriNexa Ops Agent).
- **Example value:** `trinexa-ops-agent`

---

## ✅ Setup Checklist

1. **Copy** `.env.example` → `.env` (locally).
2. Fill in:
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_LOCATION`
   - All `AZURE_OPENAI_DEPLOYMENT_*` values.
3. **Add the same variables** (with real values) as **GitHub Repo Secrets**.
4. (If using Streamlit Cloud) Add them to **Streamlit App Secrets**.
5. Run the env validator (see `backend/utils/check_env.py`) to confirm nothing is missing.

---

## 🧪 Troubleshooting

- **Error: missing environment variable**  
  → Check `.env` locally, GitHub Secrets in CI, and Streamlit Secrets in prod.

- **Error: 401 / unauthorized when calling Azure**  
  → Confirm `AZURE_OPENAI_API_KEY` is correct and matches the selected resource.

- **Error: model/deployment not found**  
  → Verify that `AZURE_OPENAI_DEPLOYMENT_*` matches the model name in Foundry exactly (case-sensitive).

---
