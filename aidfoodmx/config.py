import os
from dotenv import load_dotenv
class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///aidfoodmx.db'
# Accessing GEMINI_API_KEY from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') 

