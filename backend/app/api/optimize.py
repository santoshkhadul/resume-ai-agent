
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.optimizer import analyze_allowed_changes
from app.services.optimizer.change_manager import (
    validate_selected_keywords,
    apply_selected_keywords,
)


router = APIRouter(
    prefix="/optimize",
    tags=["Resume Optimization"],
)


class OptimizationRequest(BaseModel):
    resume_text: str = Field(..., min_length=1)
    jd_keywords: list[str] = Field(default_factory=list)


class KeywordSelectionRequest(BaseModel):
    resume_text: str = Field(..., min_length=1)
    selected_keywords: list[str] = Field(default_factory=list)
    jd_keywords: list[str] = Field(default_factory=list)


class ApplyKeywordsRequest(BaseModel):
    resume_text: str = Field(..., min_length=1)
    selected_keywords: list[str] = Field(default_factory=list)
    jd_keywords: list[str] = Field(default_factory=list)


@router.post("/analyze")
def analyze_optimization(request: OptimizationRequest):
    """Analyze JD keywords against the entire resume."""

    return analyze_allowed_changes(
        resume_text=request.resume_text,
        jd_keywords=request.jd_keywords,
    )


@router.post("/select-keywords")
def select_keywords(request: KeywordSelectionRequest):
    """Validate keywords explicitly selected by the user."""

    return validate_selected_keywords(
        resume_text=request.resume_text,
        selected_keywords=request.selected_keywords,
        jd_keywords=request.jd_keywords,
    )


@router.post("/apply-keywords")
def apply_keywords(request: ApplyKeywordsRequest):
    """Validate selected keywords before any document editing."""

    return apply_selected_keywords(
        resume_text=request.resume_text,
        selected_keywords=request.selected_keywords,
        jd_keywords=request.jd_keywords,
    )
