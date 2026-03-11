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
    github_skills:set,
    cf_score:int) -> int:
        score = 0

        # Resume presence
        if skill in resume_skills:
            score += WEIGHTS["resume"]

        if skill in project_skills:
            score += WEIGHTS["project"]

        # Certification support
        if skill in certified_skills:
            score += WEIGHTS["certification"]

        # Github support
        if skill in github_skills:
            score+=WEIGHTS["Github"]
        
        # CF applies ONLY to CS fundamentals
        if skill.lower() in CS_FUNDAMENTALS:
            score += cf_score

        return min(score,MAX_CONFIDENCE)
