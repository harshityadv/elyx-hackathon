import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'elyx-healthcare-secret-key-2025'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///elyx_healthcare.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ollama configuration
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL') or 'http://localhost:11434'
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL') or 'llama3.1:8b'

    # Member configuration
    MEMBER_NAME = "Rohan Patel"
    MEMBER_AGE = 46
    MEMBER_LOCATION = "Singapore"
    MEMBER_OCCUPATION = "Regional Head of Sales - FinTech"
