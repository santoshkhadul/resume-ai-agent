import re


def keyword_in_text(keyword: str, text: str) -> bool:
    """
    Check whether a keyword exists in text using
    safe word/phrase matching.
    """

    if not keyword or not text:
        return False

    pattern = r"(?<!\w)" + re.escape(keyword.lower()) + r"(?!\w)"

    return bool(re.search(pattern, text.lower()))


def match_keywords(
    resume_text: str,
    jd_keywords: list[str],
) -> dict:
    """
    Compare JD keywords against resume text.

    Returns matched and missing keywords.
    """

    if not resume_text:
        return {
            "matched": [],
            "missing": jd_keywords,
            "match_percentage": 0.0,
        }

    matched = []
    missing = []

    for keyword in jd_keywords:
        if keyword_in_text(keyword, resume_text):
            matched.append(keyword)
        else:
            missing.append(keyword)

    total_keywords = len(jd_keywords)

    if total_keywords == 0:
        match_percentage = 0.0
    else:
        match_percentage = round(
            (len(matched) / total_keywords) * 100,
            2,
        )

    return {
        "matched": matched,
        "missing": missing,
        "match_percentage": match_percentage,
    }