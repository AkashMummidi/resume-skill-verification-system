from utils.skill_categories import SKILL_CATEGORY_MAP
from utils.category_roadmaps import CATEGORY_ROADMAPS
from utils.task_blueprint import TASK_BLUEPRINTS, TASK_BLOCK_MAP

STATUS_PRIORITY = {
    "Missing": 4,
    "Weak Evidence": 3,
    "Moderate Evidence": 2,
    "Strong Evidence": 1
}


# -------------------------
# GET TOPICS BASED ON CONFIDENCE
# -------------------------
def get_topics_by_confidence(category, confidence):

    roadmap = CATEGORY_ROADMAPS.get(category, CATEGORY_ROADMAPS["default"])

    topics = []

    if confidence < 30:
        topics.extend(roadmap["basic"])
        topics.extend(roadmap["intermediate"])

    elif confidence < 70:
        topics.extend(roadmap["intermediate"])
    else:
        topics.extend(roadmap["advanced"])

    if confidence < 70:
        topics.extend(roadmap["advanced"])

    return topics


# -------------------------
# TOPIC PIPELINE
# -------------------------
def generate_topic_pipeline(skill, topic_data, confidence):

    topic = topic_data["topic"]
    task_type = topic_data.get("type", "practice")

    blueprint = TASK_BLUEPRINTS.get(topic, {})
    pipeline = []

    # -------------------------
    # LOW CONFIDENCE (<40)
    # -------------------------
    if confidence < 40:

        if "learn" in blueprint:
            for item in blueprint["learn"]:
                pipeline.append({
                    "task": item["task"],
                    "blocks": TASK_BLOCK_MAP[item["level"]]
                })

        if "practice" in blueprint:
            for item in blueprint["practice"]:
                pipeline.append({
                    "task": item["task"],
                    "blocks": TASK_BLOCK_MAP[item["level"]]
                })

        if "build" in blueprint:
            for item in blueprint["build"]:
                pipeline.append({
                    "task": item["task"],
                    "blocks": TASK_BLOCK_MAP[item["level"]]
                })

    # -------------------------
    # MEDIUM CONFIDENCE
    # -------------------------
    elif confidence < 70:

        if "practice" in blueprint:
            for item in blueprint["practice"]:
                pipeline.append({
                    "task": item["task"],
                    "blocks": TASK_BLOCK_MAP[item["level"]]
                })

        if "build" in blueprint:
            for item in blueprint["build"]:
                pipeline.append({
                    "task": item["task"],
                    "blocks": TASK_BLOCK_MAP[item["level"]]
                })

    # -------------------------
    # HIGH CONFIDENCE
    # -------------------------
    else:

        if "practice" in blueprint:
            for item in blueprint["practice"]:
                if item["level"] != "small":
                    pipeline.append({
                        "task": item["task"],
                        "blocks": TASK_BLOCK_MAP[item["level"]]
                    })

    # -------------------------
    # SMART FALLBACK
    # -------------------------
    if not pipeline:

        if topic in ["syntax", "control_flow", "functions"]:
            pipeline.append({
                "task": f"Learn and practice {topic} in {skill}",
                "blocks": 1
            })

        elif topic in ["oop", "file_handling"]:
            pipeline.append({
                "task": f"Practice {topic} with small programs in {skill}",
                "blocks": 2
            })

        else:
            pipeline.append({
                "task": f"Practice {topic} with real problems in {skill}",
                "blocks": 2
            })

    return pipeline


# -------------------------
# MAIN PLAN
# -------------------------
def generate_preparation_plan(skill_gap_report, total_days, hours_per_day):

    total_slots = total_days * hours_per_day
    tasks = []

    sorted_skills = sorted(
        skill_gap_report.items(),
        key=lambda x: (
            STATUS_PRIORITY.get(x[1]["status"], 1),
            -x[1]["confidence"]
        ),
        reverse=True
    )

    current_slots = 0

    for skill, data in sorted_skills:

        confidence = data["confidence"]
        category = SKILL_CATEGORY_MAP.get(skill.lower(), "default")

        topics = get_topics_by_confidence(category, confidence)

        for topic_data in topics:

            pipeline = generate_topic_pipeline(skill, topic_data, confidence)

            for task_data in pipeline:

                if current_slots >= total_slots:
                    return tasks

                tasks.append({
                    "task": task_data["task"],
                    "skill": skill,
                    "priority": 1,
                    "blocks": task_data["blocks"],
                    "completed": False
                })

                current_slots += 1

    return tasks