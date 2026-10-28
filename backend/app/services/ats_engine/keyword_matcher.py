def calculate_keyword_score(
    matched_count: int,
    total_keywords: int,
) -> float:
    """
    Calculate the ATS keyword match score.

    Returns a percentage between 0 and 100.
    """

    if total_keywords <= 0:
        return 0.0

    score = (matched_count / total_keywords) * 100

    return round(score, 2)