
from fastapi import FastAPI

from app.api.job import router as job_router
from app.api.ats import router as ats_router
from app.api.optimize import router as optimize_router
from app.api.documents import router as documents_router


app = FastAPI(
    title="Resume AI Agent",
    description="AI-powered resume analysis and optimization API",
    version="1.0.0",
)


# Register API routers
app.include_router(job_router)
app.include_router(ats_router)
app.include_router(optimize_router)
app.include_router(documents_router)


@app.get("/")
def home():
    return {
        "message": "Resume AI Agent is running",
        "status": "success",
    }
