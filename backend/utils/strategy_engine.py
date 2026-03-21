from utils.skill_categories import SKILL_CATEGORY_MAP
from utils.task_blueprint import TASK_BLUEPRINTS
import random

STRATEGIES = {
    "cs_fundamentals": ["learn", "practice", "test", "review"],
    "backend_language": ["learn", "build", "optimize"],
    "frontend_framework": ["learn", "build", "integrate"],
    "database": ["learn", "practice", "optimize"],
    "default": ["learn", "practice"]
}


def get_stage(confidence, category):
    stages = STRATEGIES.get(category, STRATEGIES["default"])

    if confidence < 30:
        return stages[0]
    elif confidence < 60:
        return stages[1]
    else:
        return stages[min(2, len(stages)-1)]


def generate_task(
    skill,
    topic,
    category,
    stage,
    confidence,
    task_type=None,
    count=None,
    difficulty=None
):

    # -------------------------
    # USE BLUEPRINT IF EXISTS
    # -------------------------
    topic_data = TASK_BLUEPRINTS.get(topic)

    if topic_data:
        stage_tasks = topic_data.get(stage)

        if stage_tasks:
            task = random.choice(stage_tasks)

            # realistic block mapping
            if "Solve" in task:
                blocks = 2
            elif "Implement" in task:
                blocks = 2
            elif "Build" in task:
                blocks = 3
            else:
                blocks = 1

            return {
                "task": f"{task} ({skill})",
                "blocks": blocks
            }

    # -------------------------
    # FALLBACK (CLEANED)
    # -------------------------
    if task_type == "learning":
        return {"task": f"Learn {topic} in {skill}", "blocks": 1}

    elif task_type == "practice":
        return {"task": f"Practice {topic} in {skill}", "blocks": 2}

    elif task_type == "build":
        return {"task": f"Build a feature using {topic} in {skill}", "blocks": 3}

    elif task_type == "optimize":
        return {"task": f"Improve performance of {topic} in {skill}", "blocks": 2}

    return {"task": f"Practice {skill}", "blocks": 1}