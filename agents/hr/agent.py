import yaml
from pathlib import Path


class HRAgent:
    """
    HR Agent responsible for PTO, benefits, onboarding, compliance questions.
    Uses policy-aware reasoning based on synthetic HR policies.
    """

    def __init__(self):
        policy_file = (
            Path(__file__).parent.parent.parent
            / "data"
            / "hr_policies.yaml"
        )
        with open(policy_file, "r", encoding="utf-8") as f:
            self.policies = yaml.safe_load(f)

        self.agent_name = "HR Agent"

    # --------------------------------------------------------------------------
    # Retrieval Layer
    # --------------------------------------------------------------------------
    def _match_policy(self, text: str) -> dict:
        text = text.lower()

        if any(k in text for k in ["pto", "vacation", "annual leave", "time off"]):
            return {
                "topic": "Paid Time Off (PTO)",
                "content": self.policies.get("pto_policy"),
            }

        if any(k in text for k in ["sick", "illness", "medical"]):
            return {
                "topic": "Sick Leave",
                "content": self.policies.get("sick_leave_policy"),
            }

        if any(k in text for k in ["benefit", "health", "dental", "vision", "insurance"]):
            return {
                "topic": "Employee Benefits",
                "content": self.policies.get("benefits_policy"),
            }

        if any(k in text for k in ["onboarding", "new hire", "orientation", "i-9"]):
            return {
                "topic": "Onboarding Requirements",
                "content": self.policies.get("onboarding_policy"),
            }

        return {"topic": None, "content": None}

    # --------------------------------------------------------------------------
    # Reasoning Layer
    # --------------------------------------------------------------------------
    def answer(self, text: str) -> dict:
        """
        Returns structured HR guidance based on matched policy.
        Output is consistent with AgentResponse requirements.
        """
        match = self._match_policy(text)

        if not match["content"]:
            return {
                "agent_name": self.agent_name,
                "department": "HR",
                "summary": "Your question appears to be HR-related, but no specific policy matched.",
                "steps": "Escalate to HR Support for review.",
            }

        policy_yaml = yaml.dump(match["content"], sort_keys=False)

        return {
            "agent_name": self.agent_name,
            "department": "HR",
            "summary": f"According to the HR policy on {match['topic']}:",
            "steps": policy_yaml,
        }
