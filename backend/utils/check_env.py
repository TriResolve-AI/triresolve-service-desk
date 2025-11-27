"""
Startup validator script that checks for required environment variables
before the application starts.

Usage:
    python -m backend.utils.check_env
"""

import os
import sys

# Required environment variables for the application
REQUIRED_ENV_VARS = [
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY",
]

# Optional environment variables with defaults
OPTIONAL_ENV_VARS = [
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
    Check if all required environment variables are set.

    Returns:
        bool: True if all required variables are set, False otherwise.
    """
    missing = []
    for var in REQUIRED_ENV_VARS:
        if not os.environ.get(var):
            missing.append(var)

    if missing:
        print("ERROR: Missing required environment variables:")
        for var in missing:
            print(f"  - {var}")
        print("\nPlease set these variables before starting the application.")
        print("See .env.example for reference.")
        return False

    print("All required environment variables are set.")

    # Check optional variables and warn if not set
    missing_optional = []
    for var in OPTIONAL_ENV_VARS:
        if not os.environ.get(var):
            missing_optional.append(var)

    if missing_optional:
        print("\nWARNING: The following optional environment variables are not set:")
        for var in missing_optional:
            print(f"  - {var}")

    return True


if __name__ == "__main__":
    if not check_env():
        sys.exit(1)
    sys.exit(0)
