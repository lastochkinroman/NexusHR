from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints.candidates import router as candidates_router

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(candidates_router, prefix="/api/v1/candidates", tags=["Candidates"])

@app.get("/health")
def health_check():
    return {
        "status": "ok", 
        "project_name": settings.PROJECT_NAME,
        "details": "Server is running!"
    }
