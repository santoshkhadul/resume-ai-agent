from app.services.document_service import extract_text
from app.utils.text_normalizer import normalize_text


def get_resume_text(file_path: str) -> str:
    """
    Extract and normalize resume text for analysis.
    """

    raw_text = extract_text(file_path)

    return normalize_text(raw_text)