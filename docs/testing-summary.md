# TriResolve AI — End-to-End Test Summary
This document contains the E2E test matrix for the TriResolve AI Multi-Agent Service Desk Orchestrator.  
The purpose is to validate domain classification, agent routing, runbook execution, and final ticket resolution across IT, HR, and Finance.

Each test case includes:  
- User-submitted ticket  
- Expected domain  
- Expected agent  
- Expected runbook  
- Expected outcome  
- Actual result  
- Pass/Fail status  

---

## 🔵 IT Domain — E2E Test Matrix

| ID   | User Ticket | Expected Domain | Expected Agent | Expected Runbook | Expected Outcome | Actual Result | Status |
|------|-------------|------------------|----------------|------------------|------------------|---------------|--------|
| **IT-1** | "I forgot my laptop password and I'm locked out." | IT | IT Agent | `password_reset_v2` | Validate identity → check lockout → reset password → notify user |  |  |
| **IT-2** | "My VPN disconnects every time I try to log in from home." | IT | IT Agent | `vpn_troubleshooting` | Diagnose VPN client → test connection → resolution or escalation |  |  |
| **IT-3** | "I need Adobe Acrobat Pro installed." | IT | IT Agent | `software_installation` | Validate license → OS compatibility → installation |  |  |
| **IT-4** | "I need access to the Finance shared drive." | IT | IT Agent | `access_permissions` | Check user role → require approval → grant access |  |  |
| **IT-5** | "My Outlook isn’t syncing emails." | IT | IT Agent | `email_sync` | Check mailbox size → restart client → test server connection |  |  |

---

## 🟣 HR Domain — E2E Test Matrix

| ID   | User Ticket | Expected Domain | Expected Agent | Expected Runbook | Expected Outcome | Actual Result | Status |
|------|-------------|------------------|----------------|------------------|------------------|---------------|--------|
| **HR-1** | "Do I have enough PTO to take 5 days next month?" | HR | HR Agent | `pto_policy` | Check balance → accrual rules → approval steps |  |  |
| **HR-2** | "I need to add my newborn to my health insurance." | HR | HR Agent | `benefits_enrollment` | Validate life event → 30-day window → required documents |  |  |
| **HR-3** | "I'm starting Monday. What are the onboarding steps?" | HR | HR Agent | `onboarding_policy` | Orientation timeline → forms → equipment → training |  |  |
| **HR-4** | "How many sick days do I get per year?" | HR | HR Agent | `sick_leave_policy` | Explain sick days → doctor's note requirements → partial day rules |  |  |
| **HR-5** | "Can I work remotely three days a week?" | HR | HR Agent | `remote_policy` | Determine eligibility → approval workflow |  |  |

---

## 🟢 Finance Domain — E2E Test Matrix

| ID   | User Ticket | Expected Domain | Expected Agent | Expected Runbook | Expected Outcome | Actual Result | Status |
|------|-------------|------------------|----------------|------------------|------------------|---------------|--------|
| **FIN-1** | "Can I get reimbursed for a $198 client lunch?" | Finance | Finance Agent | `expense_policy` | Validate amount → receipt rules → approval steps |  |  |
| **FIN-2** | "What’s the status of invoice #77821?" | Finance | Finance Agent | `invoice_status` | Retrieve invoice → approval state → payment timeline |  |  |
| **FIN-3** | "My paycheck is lower this cycle. Why?" | Finance | Finance Agent | `payroll_inquiry` | Compare periods → show deductions → explain discrepancies |  |  |
| **FIN-4** | "How much Q4 training budget is left?" | Finance | Finance Agent | `budget_tracking` | Retrieve allocation → subtract expenses → return balance |  |  |
| **FIN-5** | "My travel reimbursement hasn’t been paid yet." | Finance | Finance Agent | `expense_followup` | Check approval queue → AP status → payout date |  |  |

---

## ✔ Summary & Next Steps

### **Total Test Cases:** 15  
- 5 IT  
- 5 HR  
- 5 Finance  

### **What to Verify During Testing**
1. **Domain classification**  
   - Ticket correctly categorized into IT / HR / Finance.

2. **Agent selection**  
   - Correct domain agent is invoked.

3. **Runbook execution**  
   - The workflow matches expected steps.  
   - Deterministic YAML steps executed correctly.

4. **Final resolution**  
   - Response is clear, structured, and policy-aligned.  
   - Includes reasoning trace for judges.

5. **UI visualization**  
   - Displays classification, agent, runbook, and reasoning trace.

6. **Regression Logging**  
   - Any failures or unexpected behaviors → create GitHub issue.  
   - Include logs, ticket text, and steps to reproduce.

---

## 📝 Known Gaps (to be updated during testing)

- None documented yet.
- Add items here as issues are discovered.

---

**End of E2E Testing Summary**
