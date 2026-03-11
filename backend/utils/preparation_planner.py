from utils.skill_categories import SKILL_CATEGORY_MAP
from utils.category_roadmaps import CATEGORY_ROADMAPS


STATUS_PRIORITY = {
    "Missing": 4,
    "Weak Evidence": 3,
    "Moderate Evidence": 2,
    "Strong Evidence": 1
}


SKILL_DIFFICULTY = {
    "python": 3,
    "java": 3,
    "c": 3,

    "react": 3,
    "javascript": 2,

    "sql": 2,

    "html": 1,
    "css": 1,

    "data structures": 4,
    "algorithms": 4
}
LEVEL_ORDER = ["basic", "intermediate", "advanced"]

def generate_syllabus(skill, status, allocated_hours):

    skill_l = skill.lower()

    category = SKILL_CATEGORY_MAP.get(skill_l)

    if not category:
        return ["Study core concepts and build a small project"]

    roadmap = CATEGORY_ROADMAPS[category]

    # Starting level based on skill status
    if status == "Missing":
        start_level = "basic"

    elif status == "Weak Evidence":
        start_level = "basic"

    elif status == "Moderate Evidence":
        start_level = "intermediate"

    else:
        start_level = "advanced"

    # Max level based on available time
    if allocated_hours < 5:
        max_level = "basic"

    elif allocated_hours < 12:
        max_level = "intermediate"

    else:
        max_level = "advanced"

    # Convert to indices
    start_index = LEVEL_ORDER.index(start_level)
    max_index = LEVEL_ORDER.index(max_level)

    if max_index < start_index:
        max_index = start_index

    topics = []

    for level in LEVEL_ORDER[start_index:max_index + 1]:
        topics.extend(roadmap[level])

    syllabus = [t.format(skill=skill) for t in topics]

    return syllabus


def generate_preparation_plan(
    skill_gap_report: dict,
    days_until_interview: int,
    hours_per_day: int
):

    total_hours = days_until_interview * hours_per_day

    skill_weights = {}
    total_weight = 0

    for skill, data in skill_gap_report.items():

        status = data["status"]

        priority = STATUS_PRIORITY.get(status, 1)
        difficulty = SKILL_DIFFICULTY.get(skill.lower(), 2)

        weight = priority * difficulty

        skill_weights[skill] = weight
        total_weight += weight

    preparation_plan = {}

    for skill, weight in skill_weights.items():

        allocated_hours = (weight / total_weight) * total_hours

        status = skill_gap_report[skill]["status"]

        syllabus = generate_syllabus(skill,status, allocated_hours)

        preparation_plan[skill] = {
            "allocated_hours": round(allocated_hours, 1),
            "syllabus": syllabus
        }

    return preparation_plan