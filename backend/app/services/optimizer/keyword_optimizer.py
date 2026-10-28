import re


def keyword_in_text(keyword: str, text: str) -> bool:
    """
    Check whether a keyword or phrase exists in text.
    """

    if not keyword or not text:
        return False

    pattern = (
        r"(?<!\w)"
        + re.escape(keyword.lower())
        + r"(?!\w)"
    )

    return bool(re.search(pattern, text.lower()))


def find_safe_keyword_additions(
    resume_text: str,
    jd_keywords: list[str],
) -> list[str]:
    """
    Find JD keywords that are missing from the resume.

    This function only identifies missing keywords.
    It does NOT claim that the keywords are supported
    by the candidate's experience.
    """

    if not resume_text or not jd_keywords:
        return []

    missing_keywords = []

    for keyword in jd_keywords:
        if not keyword_in_text(keyword, resume_text):
            missing_keywords.append(keyword)

    return missing_keywords

def add_selected_keywords(
    resume_text: str,
    selected_keywords: list[str],
) -> str:
    """
    Add user-selected keywords to the resume text.

    Keywords are added to a dedicated optimization line.
    The original resume text is preserved.
    """

    if not resume_text:
        return resume_text

    if not selected_keywords:
        return resume_text

    unique_keywords = []

    for keyword in selected_keywords:
        clean_keyword = keyword.strip()

        if clean_keyword and clean_keyword not in unique_keywords:
            unique_keywords.append(clean_keyword)

    if not unique_keywords:
        return resume_text

    keyword_line = (
        "\n\nAdditional Keywords: "
        + ", ".join(unique_keywords)
    )

    return resume_text.rstrip() + keyword_line