def generate_syllabus(skill, hours):

    skill_l = skill.lower()

    category = SKILL_CATEGORY.get(skill_l)

    if not category or category not in CATEGORY_ROADMAPS:
        return ["Study core concepts and build a small project"]

    if hours < 5:
        level = "basic"
    elif hours < 12:
        level = "intermediate"
    else:
        level = "advanced"

    roadmap = CATEGORY_ROADMAPS[category][level]

    syllabus = [step.format(skill=skill) for step in roadmap]

    return syllabus