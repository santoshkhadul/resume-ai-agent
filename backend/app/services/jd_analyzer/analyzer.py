from app.services.jd_analyzer.extractor import (
    detect_sections,
    extract_keywords,
)

from app.services.jd_analyzer.matcher import match_keywords


def analyze_job_description(
    jd_text: str,
    resume_text: str = "",
) -> dict:
    """
    Analyze a job description and optionally compare it
    with resume text.
    """

    sections = detect_sections(jd_text)

    keywords = extract_keywords(jd_text)

    result = {
        "sections": sections,
        "keywords": keywords,
    }

    if resume_text:
        keyword_match = match_keywords(
            resume_text,
            keywords,
        )

        result["keyword_match"] = keyword_match

    return result