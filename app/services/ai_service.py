import os
import json
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("MODEL_NAME")
)

prompt = ChatPromptTemplate.from_template("""
You are an AI Quality Assurance Specialist.

Analyze the following customer complaint.

Complaint:
{complaint}

Return ONLY valid JSON in this format:

{{
    "summary":"",
    "category":"",
    "severity":"",
    "root_cause":"",
    "capa":"",
    "suggested_response":""
}}

Do not include markdown.
Do not include explanation.
Return only JSON.
""")

chain = prompt | llm


def analyze_complaint(complaint: str):

    result = chain.invoke(
        {
            "complaint": complaint
        }
    )

    content = result.content.strip()

    # Remove markdown code fences if present
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()

    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    return json.loads(content)