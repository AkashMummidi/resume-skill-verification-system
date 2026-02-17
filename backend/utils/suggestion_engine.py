from utils.skill_categories import SKILL_CATEGORY_MAP
from utils.action_templates import ACTION_TEMPLATES
from utils.confidence_levels import get_confidence_level

def generate_skill_suggestion(skill: str, confidence: int) -> str:
    skill_l = skill.lower()

    category = SKILL_CATEGORY_MAP.get(skill_l)
    if not category:
        return "Improve practical usage and understanding of this skill"

    confidence_level = get_confidence_level(confidence)

    template = ACTION_TEMPLATES[category][confidence_level]
    return template.format(skill=skill)
