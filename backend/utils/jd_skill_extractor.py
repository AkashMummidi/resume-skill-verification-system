from utils.resume_skill_extractor import extract_skills_from_resume

def extract_skills_from_jd(jd_text: str) -> set[str]:
    """
    Extract and from a Job Description.
    """
    jd_skills = extract_skills_from_resume(jd_text)

    return set(jd_skills)
