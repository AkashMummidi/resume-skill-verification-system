from fastapi import FastAPI, UploadFile, File
from utils.pdf_reader import extract_pdf_text
from utils.skill_normalizer import normalize_skills
from utils.resume_skill_extractor import extract_skills_from_resume
from utils.confidence_engine import compute_skill_confidence
from utils.certification_skills_extractor import extract_certified_skills
from utils.project_skills_extractor import extract_project_skills
from utils.section_extractor import extract_section
from utils.github_skills_extractor import extract_github_skills,REPO_BASE_PATH
from utils.jd_skill_extractor import extract_skills_from_jd
from utils.jd_gap_analyzer import analyze_jd_skill_gap
from utils.suggestion_engine import generate_skill_suggestion
import os

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Backend running"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are supported"}
    
    extracted_text=extract_pdf_text(file)
    
    raw_skills = extract_skills_from_resume(extracted_text)

    normalized_skills=set(normalize_skills(raw_skills)) #Skills of the resume


    project_skills=extract_project_skills(extracted_text,normalized_skills) # Skills mentioned in the project
    certified_skills=extract_certified_skills(extracted_text,normalized_skills) # skills extracted from certifications
    
    repo_path = os.path.join(REPO_BASE_PATH, "candidate_repo")

    github_skills = extract_github_skills(repo_path) # skills backed by github


    # 3. Compute confidence per skill
    confidence_map = {}

    for skill in normalized_skills:
        confidence_map[skill] = compute_skill_confidence(
        skill,
        normalized_skills,
        project_skills,
        certified_skills,
        github_skills
    )

    skill_gap_report = {}

    for skill, confidence in confidence_map.items():
        suggestion = generate_skill_suggestion(skill, confidence)

        skill_gap_report[skill] = {
            "confidence": confidence,
            "status": (
                "Missing" if confidence == 0 else
                "Weak Evidence" if confidence < 40 else
                "Moderate Evidence" if confidence < 70 else
                "Strong Evidence"
            ),
            "suggested_action": suggestion
        }


    return {
        "filename": file.filename,
        "Confidence_rating":confidence_map,
        "skill_gap":skill_gap_report
    }


@app.post("/analyze-jd")
async def analyze_jd(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...)
):
    # --- Validate ---
    if not resume_file.filename.lower().endswith(".pdf"):
        return {"error": "Resume must be a PDF"}
    if not jd_file.filename.lower().endswith(".pdf"):
        return {"error": "JD must be a PDF"}

    # --- Extract text ---
    resume_text = extract_pdf_text(resume_file)
    jd_text = extract_pdf_text(jd_file)

    # --- Resume pipeline ---
    raw_skills = extract_skills_from_resume(resume_text)
    resume_skills = set(normalize_skills(raw_skills))

    project_skills = extract_project_skills(resume_text, resume_skills)
    certified_skills = extract_certified_skills(resume_text, resume_skills)

    repo_path = os.path.join(REPO_BASE_PATH, "candidate_repo")
    github_skills = extract_github_skills(repo_path)

    confidence_map = {}
    for skill in resume_skills:
        confidence_map[skill] = compute_skill_confidence(
            skill,
            resume_skills,
            project_skills,
            certified_skills,
            github_skills
        )

    # --- JD pipeline ---
    jd_raw_skills = extract_skills_from_jd(jd_text)
    jd_skills = set(normalize_skills(jd_raw_skills))

    # --- Skill gap analysis ---
    jd_gap_report = {}

    for jd_skill in jd_skills:
        if jd_skill in resume_skills:
            confidence = confidence_map.get(jd_skill, 0)
        else:
            confidence = 0  # truly missing skill

        suggestion = generate_skill_suggestion(jd_skill, confidence)

        jd_gap_report[jd_skill] = {
            "confidence": confidence,
            "status": (
                "Missing" if confidence == 0 else
                "Weak Evidence" if confidence < 40 else
                "Moderate Evidence" if confidence < 70 else
                "Strong Evidence"
            ),
            "suggested_action": suggestion
        }


    return {
        "jd_skills": sorted(jd_skills),
        "resume_skills": sorted(resume_skills),
        "skill_gap_report": jd_gap_report
    }

