RECOMMENDED_SECTIONS = [
    "summary",
    "objective",
    "skills",
    "experience",
    "education",
    "projects",
]


def check_sections(resume_sections: dict) -> dict:
    """
    Check which common resume sections are present.
    """

    if not resume_sections:
        return {
            "present": [],
            "missing": RECOMMENDED_SECTIONS,
            "score": 0.0,
        }

    normalized_sections = {
        section.lower().strip()
        for section in resume_sections
    }

    present = []
    missing = []

    for section in RECOMMENDED_SECTIONS:
        if section in normalized_sections:
            present.append(section)
        else:
            missing.append(section)

    score = round(
        (len(present) / len(RECOMMENDED_SECTIONS)) * 100,
        2,
    )

    return {
        "present": present,
        "missing": missing,
        "score": score,
    }