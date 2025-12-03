"""
Environment variable validator for TriResolve Service Desk.

This module checks that all required Azure OpenAI environment variables
are set before the application starts.
"""

import os
import sys

# Required environment variables for Azure OpenAI integration
REQUIRED_ENV_VARS = [
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_API_VERSION",
    "AZURE_LOCATION",

    # Core system agents
    "AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR",
    "AZURE_OPENAI_DEPLOYMENT_CLASSIFIER",

    # Domain agents
    "AZURE_OPENAI_DEPLOYMENT_HR",
    "AZURE_OPENAI_DEPLOYMENT_IT",
    "AZURE_OPENAI_DEPLOYMENT_FINANCE",

    # Specialist agents
    "AZURE_OPENAI_DEPLOYMENT_ARCHITECT",
    "AZURE_OPENAI_DEPLOYMENT_SECURITY",
    "AZURE_OPENAI_DEPLOYMENT_OPS",
]


def check_env() -> bool:
    """
    Check that all required environment variables are set.

    Returns:
        True if all required environment variables are set, False otherwise.
    """
    missing = []
    empty = []

    for var in REQUIRED_ENV_VARS:
        value = os.environ.get(var)
        if value is None:
            missing.append(var)
        elif str(value).strip() == "":
            empty.append(var)

    if missing or empty:
        print("\n❌  ERROR: Environment validation failed.\n")

        if missing:
            print("Missing variables:")
            for var in missing:
                print(f"  - {var}")

        if empty:
            print("\nEmpty variables (defined but blank):")
            for var in empty:
                print(f"  - {var}")

        print("\nConfigure these values in:")
        print("  • Streamlit secrets.toml (cloud deploy)")
        print("  • Local .env (development)")
        print("  • GitHub Secrets (CI)\n")

        return False

    print("✅ SUCCESS: All required environment variables are set.")
    return True


if __name__ == "__main__":
    if not check_env():
        sys.exit(1)
