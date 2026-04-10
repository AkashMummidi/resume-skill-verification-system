import requests
import os
import json
import re

API_KEY = os.getenv("GEMINI_API_KEY")


# -------------------------------
# DIFFICULTY DISTRIBUTION
# -------------------------------
def get_distribution(conf):
    if conf < 30:
        return {"easy": 0.7, "medium": 0.3, "hard": 0.0}
    elif conf < 70:
        return {"easy": 0.3, "medium": 0.5, "hard": 0.2}
    else:
        return {"easy": 0.0, "medium": 0.3, "hard": 0.7}


def compute_counts(dist, total=10):
    counts = {k: int(v * total) for k, v in dist.items()}
    remaining = total - sum(counts.values())

    for k in ["hard", "medium", "easy"]:
        if remaining <= 0:
            break
        counts[k] += 1
        remaining -= 1

    return counts


# -------------------------------
# GENERATE QUESTIONS (FIXED)
# -------------------------------
def generate_questions(skills, total_per_skill=10):

    print(skills)

    models = [
        "models/gemini-2.0-flash",
        "models/gemini-2.0-flash-001",
        "models/gemini-flash-lite-latest"
    ]

    skills_str = ", ".join(skills)

    prompt = f"""
    Generate {total_per_skill} multiple choice questions for EACH skill.

    Skills: {skills_str}

    RULES:
    - Mix of EASY, MEDIUM, HARD questions
    - Each question must be UNIQUE
    - No coding questions
    - Exactly 4 options
    - One correct answer
    - Output STRICT JSON

    FORMAT:
    {{
      "java": [...],
      "data structures": [...]
    }}
    """

    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    for model in models:
        try:
            print("TRYING MODEL:", model)

            url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={API_KEY}"

            res = requests.post(url, json=body)
            data = res.json()

            print("RESPONSE:", data)

            if "error" in data:
                print("MODEL FAILED:", data["error"]["message"])
                continue   

            if "candidates" not in data:
                print("NO CANDIDATES")
                continue

            text = data["candidates"][0]["content"]["parts"][0]["text"]

            text = re.sub(r"```json|```", "", text).strip()

            start = text.find("{")
            end = text.rfind("}") + 1

            if start == -1 or end == -1:
                print("INVALID JSON FORMAT")
                continue

            result = json.loads(text[start:end])

            print("SUCCESS WITH:", model)
            return result  

        except Exception as e:
            print("MODEL EXCEPTION:", e)
            continue

    # ONLY AFTER ALL MODELS FAIL
    print("ALL MODELS FAILED → FALLBACK")
    return {}
# -------------------------------
# VALIDATION
# -------------------------------
def validate(qs):
    valid = []

    for q in qs:
        if (
            isinstance(q, dict) and
            "question" in q and
            "options" in q and
            isinstance(q["options"], list) and
            len(q["options"]) >= 4 and
            "answer" in q
        ):
            q["options"] = q["options"][:4]
            valid.append(q)

    print("VALID AFTER FILTER:", len(valid))
    return valid


# -------------------------------
# FALLBACK
# -------------------------------
def fallback(skill, level, count):
    base_questions = [
        f"What is {skill} used for?",
        f"Which of these best describes {skill}?",
        f"Where is {skill} commonly used?",
        f"What is a key feature of {skill}?",
        f"What type of technology is {skill}?"
    ]

    result = []

    for i in range(count):
        q = base_questions[i % len(base_questions)]

        result.append({
            "question": q,
            "options": ["Concept", "Tool", "Framework", "Language"],
            "answer": "Concept"
        })

    return result