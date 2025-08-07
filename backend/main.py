from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from agents.mcq_agent import generate_mcqs
import shutil
import os

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_files(jd: UploadFile = File(...), resume: UploadFile = File(...)):
    jd_path = os.path.join(UPLOAD_DIR, jd.filename)
    resume_path = os.path.join(UPLOAD_DIR, resume.filename)

    with open(jd_path, "wb") as buffer:
        shutil.copyfileobj(jd.file, buffer)

    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # Call MCQ generation agent
    mcqs = generate_mcqs(jd_path, resume_path)
    return {"mcqs": mcqs}
