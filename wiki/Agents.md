# 🤖 Agents & Reasoning Framework

TriResolve AI uses a hybrid multi-agent system coordinated by TriNexa.

---

## 🧠 Agent Types

### **TriNexa (Global Coordinator)**

- Primary reasoning engine
- Performs task decomposition
- Routes work to the correct domain agent
- Handles escalations and combined workflows

### **IT Agent**

- Hardware/software troubleshooting
- Reset + access workflows
- Network + device diagnostics

### **HR Agent**

- Policies and compliance
- Hiring workflows
- PTO, leave, verifications

### **Finance Agent**

- Payroll
- Vendor & invoicing queries
- Approvals and exceptions

---

## 🔍 Classifier (Model 1)

- Lightweight ticket intent classifier
- Routes incoming requests to IT/HR/Finance
- Uses synthetic + curated datasets

---

## 🧩 Agent-to-Agent Collaboration (Model 2)

Examples:

- IT & HR: “Laptop setup for new hire”
- Finance & HR: “Payroll update based on job change”
- IT & Finance: “VPN access for budget approver”

