import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor

nlp = spacy.load("en_core_web_lg")

skill_extractor = SkillExtractor(
    nlp,
    SKILL_DB,
    PhraseMatcher
)

def extract_skills_from_resume(text: str):
    annotations = skill_extractor.annotate(text)

    results = annotations.get("results", {})

    skills = []

    # High-confidence matches
    for item in results.get("full_matches", []):
        skills.append(item["doc_node_value"].lower().strip())


    # Lower-confidence matches
    for item in results.get("ngram_scored", []):
        skills.append(item["doc_node_value"].lower().strip())

    return skills
