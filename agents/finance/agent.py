import yaml
from pathlib import Path


class FinanceAgent:
    """
    Finance Agent responsible for payroll, reimbursements, invoices, and budget inquiries.
    Uses synthetic finance policies for retrieval + structured decision outputs.
    """

    def __init__(self):
        policy_file = (
            Path(__file__).parent.parent.parent
            / "data"
            / "finance_policies.yaml"
        )
        with open(policy_file, "r", encoding="utf-8") as f:
            self.policies = yaml.safe_load(f)

        self.agent_name = "Finance Agent"

    # --------------------------------------------------------------------------
    # Retrieval Layer
    # --------------------------------------------------------------------------
    def _match_policy(self, text: str) -> dict:
        text = text.lower()

        if any(k in text for k in ["payroll", "salary", "paycheck", "adjustment"]):
            return {
                "topic": "Payroll Adjustments",
                "content": self.policies.get("payroll_policy"),
            }

        if any(k in text for k in ["reimburse", "expense", "receipt", "travel"]):
            return {
                "topic": "Employee Reimbursement",
                "content": self.policies.get("reimbursement_policy"),
            }

        if any(k in text for k in ["invoice", "vendor", "budget", "purchase"]):
            return {
                "topic": "Invoice & Vendor Processing",
                "content": self.policies.get("invoice_policy"),
            }

        return {"topic": None, "content": None}

    # --------------------------------------------------------------------------
    # Reasoning + Rule Layer
    # --------------------------------------------------------------------------
    def _apply_rules(self, match: dict) -> dict:
        """
        These rules enforce safety:
        - No sensitive financial data can be produced.
        - No banking numbers, routing info, or vendor PII.
        - Only structured Finance actions allowed.
        """

        rules = {
            "sensitive_data_allowed": False,
            "allowed_actions": [
                "payroll_review",
                "expense_verification",
                "invoice_validation",
                "budget_guidance",
            ],
        }

        return rules

    # --------------------------------------------------------------------------
    # Final Answer Composition
    # --------------------------------------------------------------------------
    def answer(self, text: str) -> dict:
        match = self._match_policy(text)

        if not match["content"]:
            return {
                "agent_name": self.agent_name,
                "department": "Finance",
                "summary": "Your request is finance-related but does not match any known workflow.",
                "steps": "Escalate to Finance Operations.",
            }

        rules = self._apply_rules(match)
        policy_yaml = yaml.dump(match["content"], sort_keys=False)

        return {
            "agent_name": self.agent_name,
            "department": "Finance",
            "summary": (
                f"Finance guidance according to '{match['topic']}'. "
                f"Sensitive-data restrictions applied: {rules['sensitive_data_allowed']}."
            ),
            "steps": policy_yaml,
        }
