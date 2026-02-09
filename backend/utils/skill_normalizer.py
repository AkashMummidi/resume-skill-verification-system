import re

# 1. Stop words (noise)
STOP_WORDS = {
    "skills", "skill", "education", "project",
    "projects", "computer science", "profile", "computer science","programming",
    "programming languages","web development","web technologies","web app",
    "com","innovative","professional","persist","manage tasks","career development","time management","collaboration",
    "collaborative","teamwork","communication","presentation","problem solve","problem solving","simulations",
    
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
    "nodejs": "Node.js"

}
def normalize_skills(raw_skills: list):
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

    return sorted(normalized)
