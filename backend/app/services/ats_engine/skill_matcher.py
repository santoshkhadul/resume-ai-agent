def calculate_skill_score(
    matched_skills: list[str],
    required_skills: list[str],
) -> float:
    """
    Calculate the percentage of required skills
    found in the resume.
    """

    if not required_skills:
        return 0.0

    matched_count = len(
        set(skill.lower() for skill in matched_skills)
    )

    total_count = len(
        set(skill.lower() for skill in required_skills)
    )

    if total_count == 0:
        return 0.0

    score = (matched_count / total_count) * 100

    return round(score, 2)