from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
from config.settings import settings

llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        model_provider="google_genai",
        temperature=0.3,
        google_api_key=settings.GEMINI_API_KEY
    )

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_mcqs(jd_path, resume_path):
    jd_text = extract_text_from_pdf(jd_path)
    resume_text = extract_text_from_pdf(resume_path)

    prompt = PromptTemplate(
        input_variables=["jd", "resume"],
        template='''Based on the following job description and resume, generate 5 multiple-choice technical questions relevant to the job role.
        
Job Description:
{jd}

Resume:
{resume}

List the MCQs in the following format:
1. Question
   a) Option1
   b) Option2
   c) Option3
   d) Option4
Answer: b) Option2
'''
    )
    full_prompt = prompt.format(jd=jd_text, resume=resume_text)
    result = llm(full_prompt)
    return result
