NON_RATEABLE_ENTITIES = {
    "github",
    "ibm",
    "ms office",
    "office",
}

ABSTRACT_TERMS = {
    "front end": "frontend",
    "back end": "backend",
}

CANONICAL_SKILLS = {
    "java syntax": "java",
    "java fundamentals": "java",
    "oop": "object oriented programming",
    "problem solve": "Problem Solving",
}

CS_CORE_SKILLS = {
    "data structures",
    "algorithms",
    "problem solving",
}

TOOL_SKILLS = {
    "git",
    "github",
}

def apply_skill_policy(confidence_map: dict[str, int]) -> dict[str, int]:
    
    cleaned = {}

    for skill, confidence in confidence_map.items():
        skill_l = skill.lower().strip()

        #  Drop non-rateable entities
        if skill_l in NON_RATEABLE_ENTITIES:
            continue

        #  Canonicalize skill names
        if skill_l in CANONICAL_SKILLS:
            skill_l = CANONICAL_SKILLS[skill_l]

        #  Merge duplicates (keep max confidence)
        if skill_l in cleaned:
            cleaned[skill_l] = max(cleaned[skill_l], confidence)
        else:
            cleaned[skill_l] = confidence
    return cleaned
