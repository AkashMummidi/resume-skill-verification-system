from utils.confidence_weights import WEIGHTS, MAX_CONFIDENCE

CS_FUNDAMENTALS = {
    "data structures",
    "algorithms",
    "problem solving"
}

def compute_skill_confidence(
    skill: str,
    resume_skills: set,
    project_skills: set,
    certified_skills: set,
    github_scores: dict,
    cf_score: int
) -> int:

    score = 0

    if skill in resume_skills:
        score += WEIGHTS["resume"]

    if skill in project_skills:
        score += WEIGHTS["project"]

    if skill in certified_skills:
        score += WEIGHTS["certification"]

    # GitHub evidence
    github_score = github_scores.get(skill, 0)
    score += github_score * WEIGHTS["Github"]

    if skill.lower() in CS_FUNDAMENTALS:
        score += cf_score

    return min(score, MAX_CONFIDENCE)