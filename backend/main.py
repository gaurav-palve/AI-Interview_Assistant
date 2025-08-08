from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from controllers.interview_controller import handle_interview
from utils.logger import logger
from routes import files

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_and_generate(jd: UploadFile = File(...), resume: UploadFile = File(...)):
    logger.info(f"Received upload request: JD={jd.filename}, Resume={resume.filename}")
    return await handle_interview(jd, resume)


app.include_router(files.router, prefix="/files", tags=["Files"])
