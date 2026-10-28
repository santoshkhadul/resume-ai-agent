from fastapi import APIRouter
from pydantic import BaseModel

from app.services.jd_analyzer.analyzer import analyze_job_description


router = APIRouter(
    prefix="/job",
    tags=["Job Analysis"],
)


class JobAnalysisRequest(BaseModel):
    job_description: str
    resume_text: str = ""


@router.post("/analyze")
def analyze_job(request: JobAnalysisRequest):
    """
    Analyze a job description and optionally
    compare it with resume text.
    """

    return analyze_job_description(
        jd_text=request.job_description,
        resume_text=request.resume_text,
    )