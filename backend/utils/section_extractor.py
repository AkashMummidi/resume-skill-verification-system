import re

SECTION_HEADERS = [
    "education",
    "skills",
    "projects",
    "internships",
    "certifications",
    "achievements"
]

def extract_section(text: str, target_header: str) -> str:
    lines = text.splitlines()
    target_header = target_header.lower()

    start_idx = None

    # 1. Find exact header line
    for i, line in enumerate(lines):
        if line.strip().lower() == target_header:
            start_idx = i
            break

    if start_idx is None:
        return ""

    # 2. Find next header
    end_idx = len(lines)
    for j in range(start_idx + 1, len(lines)):
        if lines[j].strip().lower() in SECTION_HEADERS:
            end_idx = j
            break

    return "\n".join(lines[start_idx + 1:end_idx])
