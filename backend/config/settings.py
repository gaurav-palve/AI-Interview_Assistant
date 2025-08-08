import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = "AIzaSyBlqGgCNQ0tUTG6cy6gpFn0tnWxRDgRj1g"#os.getenv("GEMINI_API_KEY")
    MONGO_URI="mongodb://localhost:27017"
    DB_NAME = "interview_bot"
    
settings = Settings()
