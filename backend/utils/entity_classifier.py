import re


# Tools / productivity software
TOOL_KEYWORDS = {
    "excel", "word", "powerpoint", "ms office", "office", "git","github"
}

# Resume section headers / descriptors
NOISE_KEYWORDS = {
    "basic", "certificate", "certification",
    "languages", "skills", "profile", "education"
}

# Academic / descriptive (not direct skills)
ACADEMIC_KEYWORDS = {
    "programming", "technology", "science", "engineering"
}

# ---------------- HELPERS ---------------- #

def is_noise(token: str) -> bool:
    token_l = token.lower()

    # Only symbols or formatting junk (##, ---, etc.)
    if re.match(r"^[^A-Za-z0-9]+[A-za-z]*$", token):
        return True

    # Section headers / generic resume words
    if token_l in NOISE_KEYWORDS or token_l.startswith("skill"):
        return True

    # Broken NLP subword fragments (Lee, Jav, Abc)
    if re.match(r"^[A-Z][a-z]{2}$", token):
        return True

    return False


def is_tool(token: str) -> bool:
    return token.lower() in TOOL_KEYWORDS


def is_academic(token: str) -> bool:
    token_l = token.lower()
    return any(word in token_l for word in ACADEMIC_KEYWORDS)


def is_technical_skill(token: str) -> bool:
    # Allow legitimate single-letter languages
    if token in {"C", "R"}:
        return True

    # Must contain at least one letter
    if not re.search(r"[A-Za-z]", token):
        return False

    # Too short → ambiguous
    if len(token) < 2:
        return False

    return True


# ---------------- MAIN CLASSIFIER ---------------- #

def classify_entities(tokens: list[str]) -> dict:
    result = {
        "technical_skills": [],
        "tools": [],
        "academic_terms": [],
        "noise": []
    }

    for token in tokens:
        token = token.strip()

        if not token:
            continue

        if is_noise(token):
            result["noise"].append(token)

        elif is_tool(token):
            result["tools"].append(token)

        elif is_academic(token):
            result["academic_terms"].append(token)

        elif is_technical_skill(token):
            result["technical_skills"].append(token)

        else:
            result["noise"].append(token)

    # Remove duplicates and keep output clean
    for key in result:
        result[key] = sorted(set(result[key]))

    return result
