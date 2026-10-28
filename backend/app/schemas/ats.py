
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.ats_engine import calculate_ats_result
from app.services.jd_analyzer.analyzer import analyze_job_description
from app.services.jd_analyzer.extractor import extract_required_skills
from app.services.jd_analyzer.matcher import keyword_in_text
from app.services.resume_section_service import detect_resume_sections


router = APIRouter(
    prefix="/ats",
    tags=["ATS Analysis"],
)


class ATSRequest(BaseModel):
    resume_text: str
    job_description: str


@router.post("/score")
def calculate_score(request: ATSRequest):
    # Analyze the job description
    jd_analysis = analyze_job_description(
        jd_text=request.job_description,
        resume_text=request.resume_text,
    )

    jd_keywords = jd_analysis["keywords"]
    keyword_match = jd_analysis["keyword_match"]

    # Automatically extract required skills from the JD
    required_skills = extract_required_skills(
        request.job_description
    )

    # Match required skills against the resume
    matched_skills = [
        skill
        for skill in required_skills
        if keyword_in_text(skill, request.resume_text)
    ]

    # Detect resume sections
    resume_sections = detect_resume_sections(
        request.resume_text
    )

    # Calculate scores
    result = calculate_ats_result(
        matched_keywords=keyword_match["matched"],
        jd_keywords=jd_keywords,
        matched_skills=matched_skills,
        required_skills=required_skills,
        resume_sections=resume_sections,
    )

    # Return detailed results
    result["keyword_match"] = keyword_match
    result["jd_keywords"] = jd_keywords
    result["required_skills"] = required_skills
    result["matched_skills"] = matched_skills

    return result
