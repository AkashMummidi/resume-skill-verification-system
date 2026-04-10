from utils.db import llm_cache_collection
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

    skill_key = skill.lower().strip().replace(" ", "")

    # 1. Check cache
    cached = llm_cache_collection.find_one({"skill": skill_key})

    if cached:
        print(f"CACHE HIT: {skill}")
        return cached["topics"]

    print(f"CACHE MISS → LLM CALL: {skill}")

    # 2. Call LLM
    topics = generate_llm_topics(skill)

    # 3. Store in DB
    try:
        llm_cache_collection.insert_one({
            "skill": skill_key,
            "topics": topics
        })
    except Exception as e:
        print("CACHE STORE FAILED:", e)

    return topics