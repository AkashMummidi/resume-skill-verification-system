from fastapi import FastAPI, UploadFile, File
from utils.pdf_reader import extract_pdf_text
from utils.skill_extractor import extract_skills_from_text
from utils.skill_normalizer import normalize_skills
from utils.entity_classifier import classify_entities

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Backend running"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are supported"}
    
    extracted_text=extract_pdf_text(file)
    skills=extract_skills_from_text(extracted_text)
    normalized_skills=normalize_skills(skills,extracted_text)
    final_skills=classify_entities(normalized_skills)


    return {
        "filename": file.filename,
        "text_preview":final_skills
    }
