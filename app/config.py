from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME")

EMAIL = os.getenv("EMAIL")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")