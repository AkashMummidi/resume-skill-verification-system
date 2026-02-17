import os
from utils.skill_normalizer import normalize_skills

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

REPO_BASE_PATH = os.path.join(BASE_DIR, "sample_repos", "my_project_repos")


EXTENSION_SKILL_MAP = {
    ".py": "python",
    ".java": "java",
    ".js": "javascript",
    ".sql": "sql",
    ".html": "html",
    ".css": "css",
    ".jsx":"react"
}


def extract_github_skills(repo_path: str) -> set[str]:
    """
    Extract skills based on file extensions present in a GitHub repository.
    """
    skills = set()

    for root, _, files in os.walk(repo_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in EXTENSION_SKILL_MAP:
                skills.add(EXTENSION_SKILL_MAP[ext.lower()])
    
    github_skills=normalize_skills(skills)

    return github_skills
    
