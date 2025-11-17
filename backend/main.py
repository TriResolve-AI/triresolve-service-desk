from fastapi import FastAPI
from backend.api.routes import router as api_router

app = FastAPI(
	title="TriResolve AI - Multi-Agent Service Desk",
	description="Auto-resolving IT, HR, and Finance tickets with AI agents & runbooks.",
	version="0.1.0"
)

app.include_router(api_router)

@app.get("/")
def root():
	return {"message": "TriResolve AI backend is running"}

