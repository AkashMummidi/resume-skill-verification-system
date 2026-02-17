from utils.section_extractor import extract_section
from utils.resume_skill_extractor import extract_skills_from_resume
from utils.skill_normalizer import normalize_skills

def extract_project_skills(resume_text: str, resume_skills: set[str]) -> set[str]:
    """
    Extract skills that are actually used in projects.
    """
    project_skills=set()

    # 1. Isolate project section
    project_text = extract_section(resume_text, "projects")
    if not project_text:
        return set()

    # 2. Run SkillNER on project section
    project_section_skills = extract_skills_from_resume(project_text)

    normalized_project_skills=normalize_skills(project_section_skills)

    # 3. Keep only skills already present in resume skill set
    for skill in normalized_project_skills:
        if skill in resume_skills:project_skills.add(skill)
    return project_skills
