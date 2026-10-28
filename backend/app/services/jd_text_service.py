from app.utils.text_normalizer import normalize_text


def normalize_job_description(text: str) -> str:
    """
    Normalize job description text for ATS analysis.
    """

    if not text:
        return ""

    return normalize_text(text)