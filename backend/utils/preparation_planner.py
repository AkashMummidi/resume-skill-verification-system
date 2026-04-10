from utils.skill_categories import SKILL_CATEGORY_MAP
from utils.category_roadmaps import CATEGORY_ROADMAPS
from utils.task_blueprint import TASK_BLUEPRINTS, TASK_BLOCK_MAP
from utils.llm_topics import get_cached_or_generate
from utils.dependency_scheduler import compute_dependency_level
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
        topics.extend(roadmap["advanced"])
    else:
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

        clean_topic = topic.replace("_", " ")

        if task_type == "learning":
            pipeline.append({
                "task": f"Learn {clean_topic} concepts in {skill}",
                "blocks": 1
            })

        elif task_type == "practice":
            pipeline.append({
                "task": f"Solve 3 problems on {clean_topic} ({skill})",
                "blocks": 2
            })

        elif task_type == "build":
            pipeline.append({
                "task": f"Build a mini project using {clean_topic} in {skill}",
                "blocks": 3
            })

        elif task_type == "optimize":
            pipeline.append({
                "task": f"Optimize performance of {clean_topic} in {skill}",
                "blocks": 2
            })

        else:
            pipeline.append({
                "task": f"Practice {clean_topic} in {skill}",
                "blocks": 1
            })
    return pipeline


# -------------------------
# MAIN PLAN
# -------------------------
def generate_preparation_plan(skill_gap_report, total_days, hours_per_day):

    total_slots = total_days * hours_per_day
    tasks = []

    # preserve original order
    skill_order = {skill: i for i, skill in enumerate(skill_gap_report.keys())}

    def sort_key(item):
        skill, data = item

        level = compute_dependency_level(skill.lower())  #  dependency

        return (
            level,                                         # less dependent first
            -STATUS_PRIORITY.get(data["status"], 1),        # higher status first
            data["confidence"],                             # lower confidence first
            skill_order[skill]                              #  stable order
        )

    sorted_skills = sorted(skill_gap_report.items(), key=sort_key)

    current_slots = 0
    print(sorted_skills)

    llm_topics_map = {}

    missing_skills = [
        skill for skill, _ in sorted_skills
        if skill.lower() not in SKILL_CATEGORY_MAP
    ]

    for skill in missing_skills:
        llm_topics_map[skill] = get_cached_or_generate(skill)

    

    for skill, data in sorted_skills:

        confidence = data["confidence"]

        if skill.lower() in SKILL_CATEGORY_MAP:
            category = SKILL_CATEGORY_MAP[skill.lower()]
            topics = get_topics_by_confidence(category, confidence)
        else:
            print(f"LLM fallback (cached) for skill: {skill}")
            topics = llm_topics_map.get(skill, [])
        print(topics)

        for topic_data in topics:
            if not isinstance(topic_data, dict):
                continue

            if "topic" not in topic_data or "type" not in topic_data:
                continue

            pipeline = generate_topic_pipeline(skill, topic_data, confidence)

            if not pipeline:continue

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