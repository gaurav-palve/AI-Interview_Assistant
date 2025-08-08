from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
from utils.logger import logger
from config.settings import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
collection = db["candidates"]

fs = GridFS(db)

def save_candidate_data(candidate_id, jd_file, resume_file, mcqs):
    try:
        # Store files in GridFS
        jd_file_id = fs.put(jd_file, filename=f"{candidate_id}_jd.pdf")
        resume_file_id = fs.put(resume_file, filename=f"{candidate_id}_resume.pdf")

        candidate_data = {
            "candidate_id": candidate_id,
            "jd_file_id": jd_file_id,
            "resume_file_id": resume_file_id,
            "mcqs": mcqs
        }

        db.interviews.insert_one(candidate_data)
        logger.info(f"Saved candidate {candidate_id} data to MongoDB.")
    except Exception as e:
        logger.error(f"Error saving data for candidate {candidate_id}: {e}")

def get_candidate_data(candidate_id):
    return db.interviews.find_one({"candidate_id": candidate_id})

def delete_candidate_data(candidate_id):
    db.interviews.delete_one({"candidate_id": candidate_id})

def update_mcqs(candidate_id, new_mcqs):
    db.interviews.update_one(
        {"candidate_id": candidate_id},
        {"$set": {"mcqs": new_mcqs}}
    )
    logger.info(f"Updated MCQs for candidate {candidate_id}")
