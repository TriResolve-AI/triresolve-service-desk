from fastapi import FastAPI
from backend.api import routes

app = FastAPI(
    title="TriResolve AI - Multi-Agent Service Desk",
    description="Automatic ticket classification and resolution using AI agents",
    version="1.0.0"
)

# Include API routes
app.include_router(routes.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to TriResolve AI Service Desk",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
