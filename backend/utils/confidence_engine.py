from utils.confidence_weights import WEIGHTS, MAX_CONFIDENCE

def compute_skill_confidence(
    skill: str,
    resume_skills: set,
    project_skills: set,
    certified_skills: set,
    github_skills:set) -> int:
        score = 0

        # Resume presence
        if skill in resume_skills:
            score += WEIGHTS["resume"]

        if skill in project_skills:
            score += WEIGHTS["project"]

        # Certification support
        if skill in certified_skills:
            score += WEIGHTS["certification"]

        if skill in github_skills:
            score+=WEIGHTS["Github"]

        return min(score,MAX_CONFIDENCE)
