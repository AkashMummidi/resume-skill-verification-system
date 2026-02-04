def extract_project_skills(project_text: str, known_skills: set) -> set:
    project_text = project_text.lower()
    used = set()

    for skill in known_skills:
        if skill in project_text:
            used.add(skill)

    return used
