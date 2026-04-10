from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users_collection = db["users"]
plans_collection = db["plans"]
test_scores_collection = db["test_scores"]
llm_cache_collection = db["llm_topics_cache"]

llm_cache_collection.create_index("skill", unique=True)

# =========================
# TEST SCORE STORAGE
# =========================

def save_test_score(username, skill, score):

    test_scores_collection.update_one(
        {"username": username, "skill": skill},
        {
            "$set": {
                "username": username,
                "skill": skill,
                "score": score
            }
        },
        upsert=True
    )


def get_test_score(username, skill):

    data = test_scores_collection.find_one({
        "username": username,
        "skill": skill
    })

    if data:
        return data.get("score", 0)

    return 0