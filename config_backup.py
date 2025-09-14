import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # MongoDB configuration (Atlas with comprehensive SSL bypass)
    MONGODB_SETTINGS = {
        # Primary connection string with SSL bypass parameters
        'host': 'mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority&tlsAllowInvalidCertificates=true&tlsInsecure=true',
        'connect': False,
        'ssl': True,
        'ssl_cert_reqs': None,  # Disable certificate verification
        'tlsAllowInvalidCertificates': True,
        'tlsInsecure': True,  # Additional SSL bypass
        'serverSelectionTimeoutMS': 30000,  # Increased timeout
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
