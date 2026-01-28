from transformers import pipeline

# GLOBAL model load (at import time)
ner_pipeline = pipeline(
    "ner",
    aggregation_strategy="simple",
    device=-1
)

def extract_skills_from_text(text: str):
    entities = ner_pipeline(text)
    skills = set()
    for ent in entities:
        entity_type = ent.get("entity_group", "")
        word = ent.get("word", "").strip()

        if entity_type == "MISC" and len(word) > 1:
            skills.add(word)

    return skills
