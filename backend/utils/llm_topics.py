from utils.redis_client import redis_client
import requests
import os
import json
import re

API_KEY = os.getenv("GEMINI_API_KEY")


# -------------------------------
# GENERATE TOPICS (UNSEEN SKILLS)
# -------------------------------
def generate_llm_topics(skill):

    models = [
        "models/gemini-2.0-flash",
        "models/gemini-2.0-flash-001",
        "models/gemini-flash-lite-latest"
    ]

    prompt = f"""
    Generate a structured learning roadmap for the skill: {skill}

    RULES:
    - 5 to 7 topics
    - Each topic must be practical and interview-focused
    - Use snake_case
    - Types must be one of: learning, practice, build, optimize
    - STRICT JSON ONLY (no explanation)

    FORMAT:
    [
      {{"topic": "example_topic", "type": "learning"}}
    ]
    """

    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    # TRY MULTIPLE MODELS
    for model in models:
        try:
            print("LLM TOPIC MODEL:", model)

            url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={API_KEY}"

            res = requests.post(url, json=body)
            data = res.json()

            print("RAW LLM RESPONSE:", data)

            # HANDLE API FAILURE
            if "error" in data:
                print("MODEL FAILED:", data["error"]["message"])
                continue

            if "candidates" not in data:
                print("NO CANDIDATES")
                continue

            text = data["candidates"][0]["content"]["parts"][0]["text"]

            # CLEAN MARKDOWN
            text = re.sub(r"```json|```", "", text).strip()

            #  EXTRACT JSON ARRAY
            start = text.find("[")
            end = text.rfind("]") + 1

            if start == -1 or end == -1:
                print("INVALID JSON FORMAT")
                continue

            topics = json.loads(text[start:end])

            # VALIDATE FORMAT
            valid_topics = []
            for t in topics:
                if (
                    isinstance(t, dict) and
                    "topic" in t and
                    "type" in t and
                    t["type"] in ["learning", "practice", "build", "optimize"]
                ):
                    valid_topics.append(t)

            if valid_topics:
                print("TOPICS GENERATED")
                print(valid_topics,skill)
                return valid_topics

        except Exception as e:
            print("MODEL EXCEPTION:", e)
            continue

    #  FINAL FALLBACK
    print("ALL MODELS FAILED → FALLBACK")

    return [
        {"topic": "fundamentals", "type": "learning"},
        {"topic": "core_concepts", "type": "practice"},
        {"topic": "projects", "type": "build"}
    ]

def get_cached_or_generate(skill):

    skill_key = f"llm:{skill.lower().strip()}"

    # 1. Redis check
    cached = redis_client.get(skill_key)

    if cached:
        print(f"CACHE HIT: {skill}")
        return json.loads(cached)

    print(f"CACHE MISS → LLM CALL: {skill}")

    # 2. Generate
    topics = generate_llm_topics(skill)

    # 3. Store in Redis (24h)
    redis_client.setex(
        skill_key,
        86400,
        json.dumps(topics)
    )

    return topics