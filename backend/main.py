from fastapi import FastAPI, UploadFile, File
from utils.pdf_reader import extract_pdf_text
from utils.skill_extractor import extract_skills_from_text

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

    return {
        "filename": file.filename,
        "text_preview": skills
    }
