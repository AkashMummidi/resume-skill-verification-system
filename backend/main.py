from fastapi import FastAPI, UploadFile, File
from utils.pdf_reader import extract_pdf_text
from utils.skill_normalizer import normalize_skills
from utils.entity_classifier import classify_entities
from utils.resume_skill_extractor import extract_skills_from_resume

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

    normalized_skills=normalize_skills(raw_skills)


    return {
        "filename": file.filename,
        "text_preview":normalized_skills
    }
