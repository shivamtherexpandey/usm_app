import os
import json
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQL_DB_NAME = os.getenv('SQL_DB_NAME')
    SQL_USER = os.getenv('SQL_USER')
    SQL_PASSWORD = os.getenv('SQL_PASSWORD')
    SQL_HOST = os.getenv('SQL_HOST')
    SQL_PORT = os.getenv('SQL_PORT', '3306')
    SQL_DB_URL = f"mysql+pymysql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB_NAME}"

    SECRET_KEY = os.getenv("SECRET_KEY")
    BROKER_URL = os.getenv("BROKER_URL")

    TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")
    SUMMARIZATION_LLM_MODEL = os.getenv("SUMMARIZATION_LLM_MODEL")
    SUMMARIZATION_METHOD = os.getenv('  ', 'map_reduce')
    LLM_API_KEY = os.getenv('GOOGLE_API_KEY')

    CORS_ALLOWED_ORIGINS = json.loads(os.getenv('CORS_ALLOWED_ORIGINS', '[]'))