from utils.confidence_weights import (
    WEIGHTS,
    MAX_CONFIDENCE,
    GITHUB_MAX_CONTRIBUTION,
    CF_MAX_CONTRIBUTION,
    CF_MAX_RATING
)

# Core CS skills (Codeforces applies here only)
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
) -> float:

    score = 0

    # -------------------------
    # Resume Evidence
    # -------------------------
    if skill in resume_skills:
        score += WEIGHTS["resume"]

    # -------------------------
    # Project Evidence
    # -------------------------
    if skill in project_skills:
        score += WEIGHTS["project"]

    # -------------------------
    # Certification Evidence
    # -------------------------
    if skill in certified_skills:
        score += WEIGHTS["certification"]

    # -------------------------
    # GitHub Contribution (normalized)
    # -------------------------
    github_raw = github_scores.get(skill, 0)

    # Normalize GitHub score (0–100 → scaled)
    github_scaled = min(github_raw, 100) / 100 * GITHUB_MAX_CONTRIBUTION
    score += github_scaled

    # -------------------------
    # Codeforces Contribution (only CS skills)
    # -------------------------
    if skill.lower() in CS_FUNDAMENTALS:
        cf_scaled = min(cf_score, CF_MAX_RATING) / CF_MAX_RATING * CF_MAX_CONTRIBUTION
        score += cf_scaled

    # -------------------------
    # Final Cap
    # -------------------------
    return round(min(score, MAX_CONFIDENCE), 2)