import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # MongoDB Atlas configuration (Manual - replace with your details)
    MONGODB_SETTINGS = {
        # Option 1: SSL Disabled (most compatible)
        'host': 'mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/database_name?ssl=false&retryWrites=true&w=majority',
        
        # Option 2: SSL with certificate bypass (if Option 1 doesn't work)
        # 'host': 'mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/database_name?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority',
        
        'connect': False,
        'serverSelectionTimeoutMS': 10000
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
