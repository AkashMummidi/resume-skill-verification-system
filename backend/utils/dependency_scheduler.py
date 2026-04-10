from utils.skill_dependencies import SKILL_DEPENDENCIES


def compute_dependency_level(skill, visited=None):

    if visited is None:
        visited = set()

    if skill in visited:
        return 0

    visited.add(skill)

    deps = SKILL_DEPENDENCIES.get(skill, [])

    if not deps:
        return 0

    # FIX: use copy to avoid cross-branch interference
    return 1 + max(
        compute_dependency_level(dep, visited.copy())
        for dep in deps
    )