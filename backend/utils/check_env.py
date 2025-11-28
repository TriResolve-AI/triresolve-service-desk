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
    "AZURE_LOCATION",
    "AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR",
    "AZURE_OPENAI_DEPLOYMENT_CLASSIFIER",
    "AZURE_OPENAI_DEPLOYMENT_HR",
    "AZURE_OPENAI_DEPLOYMENT_IT",
    "AZURE_OPENAI_DEPLOYMENT_FINANCE",
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
    for var in REQUIRED_ENV_VARS:
        if not os.environ.get(var):
            missing.append(var)

    if missing:
        print("ERROR: Missing required environment variables:")
        for var in missing:
            print(f"  - {var}")
        return False

    print("SUCCESS: All required environment variables are set.")
    return True


if __name__ == "__main__":
    if not check_env():
        sys.exit(1)
