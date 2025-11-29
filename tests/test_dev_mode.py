
import json
import os
import sys

import pytest

# Ensure repository root is on sys.path so the `backend` package can be
# imported when tests run from pytest.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def _import_chat_completion():
    # Import inside helper so pytest collection doesn't import Azure clients
    from backend.services.azure_client import chat_completion

    return chat_completion


def test_classifier_dev_mode_with_env_override(monkeypatch):
    monkeypatch.setenv("TRIRESOLVE_DEV_MODE", "true")
    # Provide a canned classification JSON via env
    monkeypatch.setenv(
        "TRIRESOLVE_CANNED_CLASSIFICATION",
        '{"department": "HR", "confidence": 0.88, "rationale": "Test override"}',
    )

    chat_completion = _import_chat_completion()

    # Use the legacy calling pattern: (system_prompt, user_prompt)
    out = chat_completion(
        "You are a router for a multi-department service desk. Please classify.",
        "Title: Test ticket\nDescription: Something happened",
    )

    data = json.loads(out)
    assert data["department"] == "HR"
    assert pytest.approx(data["confidence"], 0.01) == 0.88


def test_reply_dev_mode_with_env_override(monkeypatch):
    monkeypatch.setenv("TRIRESOLVE_DEV_MODE", "1")
    monkeypatch.setenv("TRIRESOLVE_CANNED_REPLY", "DEV REPLY: We'll handle it.")

    chat_completion = _import_chat_completion()

    out = chat_completion("System prompt for assistant reply", "Please help me")
    assert out == "DEV REPLY: We'll handle it."
