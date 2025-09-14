import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # MongoDB Atlas Configuration - Multiple strategies for SSL bypass
    
    # Strategy 1: Complete SSL bypass (most compatible)
    MONGODB_SETTINGS_STRATEGY_1 = {
        'host': 'mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/smart_resume?ssl=false&retryWrites=true&w=majority',
        'connect': False,
        'ssl': False,  # Completely disable SSL
        'serverSelectionTimeoutMS': 30000,
        'socketTimeoutMS': 20000,
        'connectTimeoutMS': 20000
    }
    
    # Strategy 2: SSL with certificate bypass (recommended)
    MONGODB_SETTINGS_STRATEGY_2 = {
        'host': 'mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/smart_resume?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority&tlsAllowInvalidCertificates=true&tlsInsecure=true',
        'connect': False,
        'ssl': True,
        'ssl_cert_reqs': None,
        'tlsAllowInvalidCertificates': True,
        'tlsInsecure': True,
        'serverSelectionTimeoutMS': 30000,
        'socketTimeoutMS': 20000,
        'connectTimeoutMS': 20000
    }
    
    # Strategy 3: Alternative Atlas connection (from .env file)
    MONGODB_SETTINGS_STRATEGY_3 = {
        'host': 'mongodb+srv://sweetykp23hcs_db_user:2023HC0570@smart-resume-jobmatch.iewebgp.mongodb.net/smart_resume?ssl=false&retryWrites=true&w=majority',
        'connect': False,
        'ssl': False,
        'serverSelectionTimeoutMS': 30000,
        'socketTimeoutMS': 20000,
        'connectTimeoutMS': 20000
    }
    
    # Default configuration (use Strategy 1 - most compatible)
    MONGODB_SETTINGS = MONGODB_SETTINGS_STRATEGY_1

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-key-for-smart-resume'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['cookies']

    # File upload configuration
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    @classmethod
    def switch_to_strategy(cls, strategy_number):
        """Switch MongoDB connection strategy"""
        if strategy_number == 1:
            cls.MONGODB_SETTINGS = cls.MONGODB_SETTINGS_STRATEGY_1
            print("🔄 Switched to Strategy 1: SSL completely disabled")
        elif strategy_number == 2:
            cls.MONGODB_SETTINGS = cls.MONGODB_SETTINGS_STRATEGY_2
            print("🔄 Switched to Strategy 2: SSL with certificate bypass")
        elif strategy_number == 3:
            cls.MONGODB_SETTINGS = cls.MONGODB_SETTINGS_STRATEGY_3
            print("🔄 Switched to Strategy 3: Alternative Atlas connection")
        else:
            print("❌ Invalid strategy number. Available: 1, 2, 3")
