
from app.core.policies import (
    ALLOW_KEYWORD_ADDITION,
    ALLOW_SAFE_PHRASE_REPLACEMENT,
    ALLOW_FULL_REWRITE,
)

from app.services.optimizer.evidence_checker import (
    find_keyword_evidence,
)


def analyze_allowed_changes(
    resume_text: str,
    jd_keywords: list[str],
) -> dict:
    """
    Classify JD keywords using evidence from the entire resume.

    Python in Skills:
        No change needed.

    Docker in Projects:
        Offer to add it to Skills.

    AWS not found:
        Ask the user to confirm their experience.
    """

    keyword_options = []
    seen = set()

    for keyword in jd_keywords:
        clean_keyword = keyword.strip()

        if not clean_keyword:
            continue

        normalized_keyword = clean_keyword.lower()

        if normalized_keyword in seen:
            continue

        seen.add(normalized_keyword)

        evidence = find_keyword_evidence(
            keyword=clean_keyword,
            resume_text=resume_text,
        )

        section = evidence.get("section")

        if evidence["supported"]:
            if section == "skills":
                status = "already_in_skills"
                action = "no_change_needed"
            else:
                status = "present_elsewhere"
                action = "offer_add_to_skills"

            warning = None

        else:
            status = "missing_from_resume"
            action = "request_user_confirmation"

            warning = (
                "No direct evidence found. Add this skill only "
                "if it accurately reflects your actual skills "
                "or experience."
            )

        keyword_options.append(
            {
                "keyword": clean_keyword,
                "supported": evidence["supported"],
                "evidence_type": evidence["evidence_type"],
                "section": section,
                "status": status,
                "suggested_action": action,
                "warning": warning,
                "can_user_add": ALLOW_KEYWORD_ADDITION,
            }
        )

    # Only keywords that need attention count as changes.
    change_count = sum(
        1
        for item in keyword_options
        if item["status"] != "already_in_skills"
    )

    return {
        "missing_keywords": [
            item
            for item in keyword_options
            if item["status"] != "already_in_skills"
        ],
        "keyword_options": keyword_options,
        "change_count": change_count,
        "keyword_addition_allowed": ALLOW_KEYWORD_ADDITION,
        "phrase_replacement_allowed": ALLOW_SAFE_PHRASE_REPLACEMENT,
        "full_rewrite_allowed": ALLOW_FULL_REWRITE,
    }


def validate_selected_keywords(
    resume_text: str,
    selected_keywords: list[str],
    jd_keywords: list[str],
) -> dict:
    """Accept selected JD keywords only when resume evidence exists."""

    jd_keyword_set = {
        keyword.lower().strip()
        for keyword in jd_keywords
        if keyword.strip()
    }

    valid_selections = []
    rejected_selections = []
    seen = set()

    for keyword in selected_keywords:
        clean_keyword = keyword.strip()

        if not clean_keyword:
            continue

        normalized_keyword = clean_keyword.lower()

        if normalized_keyword in seen:
            continue

        seen.add(normalized_keyword)

        if normalized_keyword not in jd_keyword_set:
            rejected_selections.append(
                {
                    "keyword": clean_keyword,
                    "reason": (
                        "Keyword is not present in the job description."
                    ),
                }
            )
            continue

        evidence = find_keyword_evidence(
            keyword=clean_keyword,
            resume_text=resume_text,
        )

        if not evidence["supported"]:
            rejected_selections.append(
                {
                    "keyword": clean_keyword,
                    "reason": (
                        "No direct evidence found in the resume. "
                        "Add it only if it accurately reflects "
                        "your actual skills or experience."
                    ),
                }
            )
            continue

        section = evidence.get("section")

        valid_selections.append(
            {
                "keyword": clean_keyword,
                "user_selected": True,
                "existing_section": section,
                "suggested_action": (
                    "no_change_needed"
                    if section == "skills"
                    else "offer_add_to_skills"
                ),
            }
        )

    return {
        "selected_keywords": valid_selections,
        "rejected_keywords": rejected_selections,
        "selected_count": len(valid_selections),
    }


def apply_selected_keywords(
    resume_text: str,
    selected_keywords: list[str],
    jd_keywords: list[str],
) -> dict:
    """
    Validate selected keywords without appending duplicate text.

    Actual DOCX/PDF Skills-section editing will be handled
    separately by the document-editing workflow.
    """

    if not ALLOW_KEYWORD_ADDITION:
        return {
            "updated_resume": resume_text,
            "selected_keywords": [],
            "rejected_keywords": [
                {
                    "keyword": keyword,
                    "reason": "Keyword addition is disabled by policy.",
                }
                for keyword in selected_keywords
            ],
            "selected_count": 0,
        }

    validation = validate_selected_keywords(
        resume_text=resume_text,
        selected_keywords=selected_keywords,
        jd_keywords=jd_keywords,
    )

    # Do not append keywords to the end of the resume.
    # This prevents duplicate keywords and accidental layout changes.
    updated_resume = resume_text

    return {
        "updated_resume": updated_resume,
        "selected_keywords": validation["selected_keywords"],
        "rejected_keywords": validation["rejected_keywords"],
        "selected_count": validation["selected_count"],
    }
