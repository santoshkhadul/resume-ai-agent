
import re

from app.services.resume_section_service import detect_resume_sections


def keyword_in_text(
    keyword: str,
    text: str,
) -> bool:
    """Check whether a keyword exists as a complete word or phrase."""

    if not keyword or not text:
        return False

    pattern = (
        r"(?<!\w)"
        + re.escape(keyword.strip().lower())
        + r"(?!\w)"
    )

    return bool(re.search(pattern, text.lower()))


def find_keyword_evidence(
    keyword: str,
    resume_text: str,
) -> dict:
    """
    Check the entire resume for keyword evidence,
    including Skills, Projects, and Experience.
    """

    if not keyword or not resume_text:
        return {
            "keyword": keyword,
            "supported": False,
            "evidence_type": None,
            "section": None,
            "reason": "Keyword or resume text is empty.",
        }

    sections = detect_resume_sections(resume_text)

    # Prefer checking recognized sections so we can
    # report where the keyword was found.
    for section_name, section_text in sections.items():
        if keyword_in_text(keyword, section_text):
            return {
                "keyword": keyword,
                "supported": True,
                "evidence_type": "direct_match",
                "section": section_name,
                "reason": (
                    f"Keyword already exists in the "
                    f"{section_name} section."
                ),
            }

    # Also check the entire resume in case the section
    # heading could not be detected.
    if keyword_in_text(keyword, resume_text):
        return {
            "keyword": keyword,
            "supported": True,
            "evidence_type": "direct_match",
            "section": None,
            "reason": (
                "Keyword already exists in the resume, "
                "but its section could not be identified."
            ),
        }

    return {
        "keyword": keyword,
        "supported": False,
        "evidence_type": None,
        "section": None,
        "reason": "No direct evidence found in the resume.",
    }
