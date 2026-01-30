import re

# 1. Stop words (noise)
STOP_WORDS = {
    "cs", "skills", "skill", "education", "project",
    "projects", "computer science", "profile"
}

# 2. Alias mapping (normalization)
SKILL_ALIAS_MAP = {
    "js": "JavaScript",
    "javascript": "JavaScript",
    "py": "Python",
    "python": "Python",
    "sql": "SQL",
    "git": "Git",
    "html": "HTML",
    "css": "CSS",
    "reactjs": "React",
    "nodejs": "Node.js",
}

# 3. Short skills frequently missed by NER
SHORT_SKILLS = {
    "html": "HTML",
    "css": "CSS",
    "c": "C",
    "c++": "C++"
}

def normalize_skills(raw_skills: list, resume_text: str):
    normalized = set()

    # ---- STEP A: Clean + normalize AI-extracted skills ----
    for skill in raw_skills:
        skill_clean = skill.strip().lower()

        if any(skill_clean == stop or skill_clean.startswith(stop) for stop in STOP_WORDS):
            continue

        if skill_clean in SKILL_ALIAS_MAP:
            normalized.add(SKILL_ALIAS_MAP[skill_clean])
        else:
            normalized.add(skill.strip())

    # ---- STEP B: Supplement missing short skills from resume text ----
    resume_text_lower = resume_text.lower()

    for short, proper in SHORT_SKILLS.items():
        if re.search(rf"\b{re.escape(short)}\b", resume_text_lower):
            normalized.add(proper)

    return sorted(normalized)
