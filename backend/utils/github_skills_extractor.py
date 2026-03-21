import requests
from collections import defaultdict
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_API = "https://api.github.com"


def _get_headers():
    if GITHUB_TOKEN:
        return {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"}
    return {}



# -----------------------------------------
# Fetch user repositories
# -----------------------------------------
def _get_user_repos(username):

    url = f"{GITHUB_API}/users/{username}/repos"

    response = requests.get(url, headers=_get_headers())

    if response.status_code != 200:
        print("GitHub API error:", response.status_code)
        print(response.text)
        return []

    return response.json()


# -----------------------------------------
# Get languages used in repository
# -----------------------------------------
def _get_repo_languages(username, repo_name):

    url = f"{GITHUB_API}/repos/{username}/{repo_name}/languages"

    response = requests.get(url, headers=_get_headers())

    if response.status_code != 200:
        return {}

    return response.json()


# -----------------------------------------
# Detect frameworks from repository files
# -----------------------------------------
def _detect_frameworks(username, repo_name):

    url = f"{GITHUB_API}/repos/{username}/{repo_name}/contents"

    response = requests.get(url, headers=_get_headers())

    if response.status_code != 200:
        return []

    files = [f["name"].lower() for f in response.json()]

    frameworks = []

    # Python ecosystem
    if "requirements.txt" in files:
        frameworks.append("python_framework")

    if "pyproject.toml" in files:
        frameworks.append("python_project")

    # JavaScript ecosystem
    if "package.json" in files:
        frameworks.append("javascript_framework")

    # Docker
    if "dockerfile" in files:
        frameworks.append("docker")

    return frameworks


# -----------------------------------------
# Check if repository is recently active
# -----------------------------------------
def _repo_is_active(repo):

    updated = repo.get("updated_at")

    if not updated:
        return False

    updated_date = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ")

    days_since_update = (datetime.utcnow() - updated_date).days

    return days_since_update < 180


# -----------------------------------------
# PUBLIC FUNCTION
# Extract GitHub skill evidence
# -----------------------------------------
def extract_github_skills(username):

    repos = _get_user_repos(username)

    language_bytes = defaultdict(int)
    repo_count = defaultdict(int)
    frameworks = set()
    active_repos = 0

    for repo in repos:

        repo_name = repo["name"]

        # Language statistics
        languages = _get_repo_languages(username, repo_name)

        for lang, bytes_of_code in languages.items():

            lang = lang.lower()

            language_bytes[lang] += bytes_of_code
            repo_count[lang] += 1

        # Framework detection
        frameworks.update(_detect_frameworks(username, repo_name))

        # Activity check
        if _repo_is_active(repo):
            active_repos += 1

    return {
        "language_bytes": dict(language_bytes),
        "repo_count": dict(repo_count),
        "frameworks": list(frameworks),
        "active_repos": active_repos
    }
def compute_github_skill_scores(github_data):

    language_bytes = github_data["language_bytes"]
    repo_count = github_data["repo_count"]
    frameworks = github_data["frameworks"]
    active_repos = github_data["active_repos"]

    scores = {}

    for skill in language_bytes:

        score = 0

        # repo count score
        repos = repo_count.get(skill, 0)

        if repos >= 4:
            score += 30
        elif repos >= 2:
            score += 20
        elif repos == 1:
            score += 10

        # lines of code score
        loc = language_bytes.get(skill, 0)

        if loc > 10000:
            score += 25
        elif loc > 2000:
            score += 15
        else:
            score += 5

        # framework score
        if skill == "python" and "python_framework" in frameworks:
            score += 15

        if skill == "javascript" and "javascript_framework" in frameworks:
            score += 15
        # activity score
        if active_repos > 0:
            score += 10

        scores[skill] = score
    print(scores)
    return scores