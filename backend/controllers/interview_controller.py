import uuid
from fastapi import UploadFile
from agents.mcq_agent import generate_mcqs
from utils.db import save_candidate_data
from utils.logger import logger
from PyPDF2 import PdfReader
import io

def extract_text_from_upload(upload_file: UploadFile):
    content = upload_file.file.read()
    reader = PdfReader(io.BytesIO(content))
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text, content

async def handle_interview(jd: UploadFile, resume: UploadFile):
    candidate_id = str(uuid.uuid4())
    logger.info(f"Started processing candidate {candidate_id}")

    # Extract text and binary content
    jd_text, jd_bytes = extract_text_from_upload(jd)
    resume_text, resume_bytes = extract_text_from_upload(resume)

    logger.debug(f"JD Text for {candidate_id}: {jd_text[:100]}")
    logger.debug(f"Resume Text for {candidate_id}: {resume_text[:100]}")

    # Generate MCQs
    mcqs = generate_mcqs(jd_text, resume_text)
    logger.info(f"Generated MCQs for candidate {candidate_id}")

    # Save all data to DB
    save_candidate_data(candidate_id, jd_bytes, resume_bytes, mcqs)

    return {"candidate_id": candidate_id, "mcqs": mcqs}
