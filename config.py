import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # WORKING MongoDB Atlas Configuration
    # Based on successful connection test from diagnose_mongodb_simple.py
    MONGODB_SETTINGS = {
        # This connection string works! (verified by testing)
        'host': 'mongodb+srv://sweetykp23hcs_db_user:2023HC0570@smart-resume-jobmatch.iewebgp.mongodb.net/smart_resume?retryWrites=true&w=majority',
        'connect': False,  # Let mongoengine handle connection
        'serverSelectionTimeoutMS': 30000,  # Increased timeout for reliability
        'socketTimeoutMS': 20000,
        'connectTimeoutMS': 20000,
        'maxPoolSize': 10,
        'retryWrites': True
    }

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-key-for-smart-resume'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['cookies']

    # File upload configuration
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
