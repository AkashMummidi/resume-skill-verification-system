from utils.section_extractor import extract_section
from utils.resume_skill_extractor import extract_skills_from_resume
from utils.skill_normalizer import normalize_skills

def extract_certified_skills(resume_text: str, resume_skills: set[str]) -> set[str]:
    """
    Extract skills that are supported by certifications.
    """

    # 1. Isolate certification section
    cert_text = extract_section(
        resume_text,
        "certifications"
    )

    if not cert_text:
        return set()

    # 2. Run SkillNER on certification section
    cert_section_skills = extract_skills_from_resume(cert_text)
    
    normalized_cert_skills=normalize_skills(cert_section_skills)

    # 3. Keep only skills already present in resume skill set
    certified_skills = {
        skill for skill in normalized_cert_skills
        if skill in resume_skills
    }

    return certified_skills
