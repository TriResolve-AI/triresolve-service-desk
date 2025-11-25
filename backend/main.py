"""
Thin wrapper so you can run:

    uvicorn backend.main:app --reload

and still keep the real FastAPI app in backend/api/main.py
"""

from backend.api.main import app  # noqa: F401
