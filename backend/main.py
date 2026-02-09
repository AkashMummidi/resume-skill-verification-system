from fastapi import FastAPI, UploadFile, File
from utils.pdf_reader import extract_pdf_text
from utils.skill_normalizer import normalize_skills
from utils.resume_skill_extractor import extract_skills_from_resume
from utils.confidence_engine import compute_skill_confidence
from utils.certification_skills_extractor import extract_certified_skills
from utils.project_skills_extractor import extract_project_skills
from utils.section_extractor import extract_section

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

    project_text=extract_section(extracted_text,"projects")

    certified_text=extract_section(extracted_text,"certifications")



    project_skills=extract_project_skills(extracted_text,normalized_skills)
    certified_skills=extract_certified_skills(extracted_text,normalized_skills)

    # 3. Compute confidence per skill
    confidence_map = {}

    for skill in normalized_skills:
        confidence_map[skill] = compute_skill_confidence(
        skill,
        normalized_skills,
        project_skills,
        certified_skills
    )


    return {
        "filename": file.filename,
        "Confidence_rating":confidence_map
    }
