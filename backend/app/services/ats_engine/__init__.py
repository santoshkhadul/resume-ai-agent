from app.services.ats_engine.keyword_matcher import calculate_keyword_score
from app.services.ats_engine.skill_matcher import calculate_skill_score
from app.services.ats_engine.section_checker import check_sections
from app.services.ats_engine.scorer import calculate_ats_score


def calculate_ats_result(
    matched_keywords: list[str],
    jd_keywords: list[str],
    matched_skills: list[str],
    required_skills: list[str],
    resume_sections: dict,
) -> dict:
    """
    Calculate the complete ATS result.
    """

    keyword_score = calculate_keyword_score(
        matched_count=len(matched_keywords),
        total_keywords=len(jd_keywords),
    )

    skill_score = calculate_skill_score(
        matched_skills=matched_skills,
        required_skills=required_skills,
    )

    section_result = check_sections(resume_sections)

    final_score = calculate_ats_score(
        keyword_score=keyword_score,
        skill_score=skill_score,
        section_score=section_result["score"],
    )

    return {
        "ats_score": final_score,
        "keyword_score": keyword_score,
        "skill_score": skill_score,
        "section_score": section_result["score"],
        "section_details": section_result,
    }