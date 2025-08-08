from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from config.settings import settings
from utils.logger import logger

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    google_api_key=settings.GEMINI_API_KEY
)

def generate_mcqs(jd_text: str, resume_text: str) -> str:
    logger.debug("Generating MCQs with extracted JD and Resume text.")
    
    prompt = PromptTemplate(
        input_variables=["jd", "resume"],
        template='''
Based on the following job description and resume, generate 5 multiple-choice technical questions relevant to the job role.

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

    formatted_prompt = prompt.format(jd=jd_text, resume=resume_text)
    messages = [HumanMessage(content=formatted_prompt)]

    logger.debug("Sending prompt to Gemini model.")
    response = llm(messages)
    logger.debug("Received response from Gemini model.")

    return response.content
