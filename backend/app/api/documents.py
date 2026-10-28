
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.optimizer.change_manager import (
    validate_selected_keywords,
)
from app.services.document_service import extract_docx_text
from app.services.document_generator.docx_generator import (
    add_keywords_to_docx_skills,
)


router = APIRouter(
    prefix="/documents",
    tags=["Resume Documents"],
)


class OptimizeDocxRequest(BaseModel):
    input_path: str = Field(..., min_length=1)
    output_path: str = Field(..., min_length=1)
    selected_keywords: list[str] = Field(default_factory=list)
    jd_keywords: list[str] = Field(default_factory=list)


@router.post("/optimize-docx")
def optimize_docx(request: OptimizeDocxRequest):
    """Create an edited DOCX copy using verified keywords."""

    source = Path(request.input_path).resolve()
    destination = Path(request.output_path).resolve()

    if not source.is_file():
        raise HTTPException(
            status_code=404,
            detail="The input DOCX file was not found.",
        )

    if source.suffix.lower() != ".docx":
        raise HTTPException(
            status_code=400,
            detail="Only DOCX input files are supported.",
        )

    if destination.suffix.lower() != ".docx":
        raise HTTPException(
            status_code=400,
            detail="The output path must end with .docx.",
        )

    if source == destination:
        raise HTTPException(
            status_code=400,
            detail="The output file must differ from the original.",
        )

    try:
        resume_text = extract_docx_text(str(source))

        validation = validate_selected_keywords(
            resume_text=resume_text,
            selected_keywords=request.selected_keywords,
            jd_keywords=request.jd_keywords,
        )

        supported_keywords = [
            item["keyword"]
            for item in validation["selected_keywords"]
            if item["suggested_action"] == "offer_add_to_skills"
        ]

        if not supported_keywords:
            return {
                "success": True,
                "message": "No new Skills keywords need to be added.",
                "output_path": None,
                "selected_keywords": validation["selected_keywords"],
                "rejected_keywords": validation["rejected_keywords"],
                "added_keywords": [],
                "skipped_keywords": [],
            }

        result = add_keywords_to_docx_skills(
            input_path=str(source),
            output_path=str(destination),
            keywords=supported_keywords,
        )

        return {
            "success": result["success"],
            "message": result["message"],
            "output_path": result["output_path"],
            "selected_keywords": validation["selected_keywords"],
            "rejected_keywords": validation["rejected_keywords"],
            "added_keywords": result["added_keywords"],
            "skipped_keywords": result["skipped_keywords"],
        }

    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not process the DOCX document.",
        ) from exc
