def calculate_ats_score(
    keyword_score: float,
    skill_score: float,
    section_score: float,
) -> float:
    """
    Calculate the overall ATS score.

    Current weights:
    - Keyword match: 50%
    - Skill match: 30%
    - Section quality: 20%
    """

    keyword_score = max(0.0, min(keyword_score, 100.0))
    skill_score = max(0.0, min(skill_score, 100.0))
    section_score = max(0.0, min(section_score, 100.0))

    final_score = (
        (keyword_score * 0.50)
        + (skill_score * 0.30)
        + (section_score * 0.20)
    )

    return round(final_score, 2)