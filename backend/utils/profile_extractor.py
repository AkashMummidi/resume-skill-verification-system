import re
from utils.pdf_link_extractor import extract_links_from_bytes


def extract_profiles(file_bytes: bytes, text: str):

    github = None
    codeforces = None

    # -------------------------
    # 1. Extract from hyperlinks (BEST)
    # -------------------------
    links = extract_links_from_bytes(file_bytes)

    for link in links:

        if "github.com" in link:
            github = link.split("github.com/")[-1].strip("/")

        if "codeforces.com" in link:
            if "profile" in link:
                codeforces = link.split("codeforces.com/profile/")[-1].strip("/")
            else:
                codeforces = link.split("codeforces.com/")[-1].strip("/")

    # -------------------------
    # 2. Fallback to text regex
    # -------------------------
    if not github:
        gh_match = re.search(r"github\.com/([A-Za-z0-9_-]+)", text)
        if gh_match:
            github = gh_match.group(1)

    if not codeforces:
        cf_match = re.search(r"codeforces\.com/(?:profile/)?([A-Za-z0-9_-]+)", text)
        if cf_match:
            codeforces = cf_match.group(1)

    return github, codeforces