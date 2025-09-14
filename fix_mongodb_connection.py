#!/usr/bin/env python3
"""
MongoDB Connection Troubleshooter for Smart Resume

This script diagnoses and fixes MongoDB connection issues, specifically SSL problems.
"""

import os
import sys
import traceback
from datetime import datetime

def test_basic_connection():
    """Test basic MongoDB connection without SSL"""
    print("🔧 TESTING BASIC MongoDB CONNECTION")
    print("="*60)
    
    try:
        import pymongo
        print("✅ PyMongo is installed")
        
        # Test local MongoDB first
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
            client.admin.command('hello')
            print("✅ Local MongoDB is available")
            return "local"
        except:
            print("ℹ️  Local MongoDB not available (this is normal)")
        
        # Test if we can connect to MongoDB Atlas with SSL fixes
        atlas_uri = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/smart_resume')
        
        if 'mongodb+srv://' in atlas_uri:
            print(f"🔍 Testing MongoDB Atlas connection...")
            
            # Try with SSL disabled first
            try:
                fixed_uri = atlas_uri + "?ssl=false&retryWrites=true&w=majority"
                client = pymongo.MongoClient(fixed_uri, serverSelectionTimeoutMS=10000)
                client.admin.command('hello')
                print("✅ MongoDB Atlas works with SSL disabled")
                return "atlas_no_ssl"
            except Exception as e:
                print(f"❌ Atlas without SSL failed: {str(e)[:100]}...")
            
            # Try with SSL certificate verification disabled
            try:
                fixed_uri = atlas_uri + "?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority"
                client = pymongo.MongoClient(fixed_uri, serverSelectionTimeoutMS=10000)
                client.admin.command('hello')
                print("✅ MongoDB Atlas works with SSL cert verification disabled")
                return "atlas_ssl_nocert"
            except Exception as e:
                print(f"❌ Atlas with SSL no cert failed: {str(e)[:100]}...")
            
            # Try with TLS 1.2 explicitly
            try:
                import ssl
                fixed_uri = atlas_uri + "?retryWrites=true&w=majority"
                client = pymongo.MongoClient(
                    fixed_uri, 
                    serverSelectionTimeoutMS=10000,
                    ssl=True,
                    ssl_cert_reqs=ssl.CERT_NONE,
                    tlsAllowInvalidCertificates=True
                )
                client.admin.command('hello')
                print("✅ MongoDB Atlas works with TLS settings")
                return "atlas_tls_fixed"
            except Exception as e:
                print(f"❌ Atlas with TLS settings failed: {str(e)[:100]}...")
        
        print("❌ No working MongoDB connection found")
        return None
        
    except ImportError:
        print("❌ PyMongo not installed - run 'pip install pymongo'")
        return None
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return None

def fix_config_file(connection_type):
    """Fix the config.py file based on working connection type"""
    print(f"\n🔧 FIXING CONFIGURATION FOR: {connection_type}")
    print("="*60)
    
    # Read current config
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            config_content = f.read()
    except:
        print("❌ Cannot read config.py")
        return False
    
    # Backup original config
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'config_backup_{timestamp}.py'
    try:
        with open(backup_name, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"✅ Backup created: {backup_name}")
    except:
        print("⚠️  Could not create backup")
    
    # Generate new MongoDB settings
    if connection_type == "local":
        mongodb_settings = """    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost:27017/smart_resume',
        'connect': False
    }"""
    elif connection_type == "atlas_no_ssl":
        mongodb_settings = """    MONGODB_SETTINGS = {
        'host': os.environ.get('DATABASE_URL', 'mongodb://localhost:27017/smart_resume') + '?ssl=false&retryWrites=true&w=majority',
        'connect': False
    }"""
    elif connection_type == "atlas_ssl_nocert":
        mongodb_settings = """    MONGODB_SETTINGS = {
        'host': os.environ.get('DATABASE_URL', 'mongodb://localhost:27017/smart_resume') + '?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority',
        'connect': False
    }"""
    elif connection_type == "atlas_tls_fixed":
        mongodb_settings = """    MONGODB_SETTINGS = {
        'host': os.environ.get('DATABASE_URL', 'mongodb://localhost:27017/smart_resume') + '?retryWrites=true&w=majority',
        'connect': False,
        'ssl': True,
        'ssl_cert_reqs': 'CERT_NONE',
        'tlsAllowInvalidCertificates': True
    }"""
    else:
        print("❌ Unknown connection type")
        return False
    
    # Replace the MongoDB settings in config
    import re
    pattern = r'MONGODB_SETTINGS = \{[^}]*\}'
    
    if re.search(pattern, config_content):
        new_config = re.sub(pattern, mongodb_settings.strip(), config_content)
        
        # Write new config
        try:
            with open('config.py', 'w', encoding='utf-8') as f:
                f.write(new_config)
            print("✅ Updated config.py with working MongoDB settings")
            return True
        except Exception as e:
            print(f"❌ Failed to write config.py: {e}")
            return False
    else:
        print("❌ Could not find MONGODB_SETTINGS in config.py")
        return False

def update_env_file(connection_type):
    """Update .env file if needed"""
    print(f"\n🔧 UPDATING .env FILE")
    print("="*60)
    
    if connection_type == "local":
        print("ℹ️  Using local MongoDB - no .env changes needed")
        return True
    
    try:
        # Read current .env
        env_content = ""
        if os.path.exists('.env'):
            with open('.env', 'r', encoding='utf-8') as f:
                env_content = f.read()
        
        # Update FLASK_ENV to FLASK_DEBUG
        if 'FLASK_ENV=development' in env_content:
            env_content = env_content.replace('FLASK_ENV=development', 'FLASK_DEBUG=True')
            print("✅ Updated FLASK_ENV to FLASK_DEBUG")
        
        # Write updated .env
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
            
        print("✅ Updated .env file")
        return True
        
    except Exception as e:
        print(f"❌ Failed to update .env: {e}")
        return False

def test_fixed_connection():
    """Test the connection after fixes"""
    print(f"\n🧪 TESTING FIXED CONNECTION")
    print("="*60)
    
    try:
        # Import and test the fixed app
        import importlib
        if 'app' in sys.modules:
            importlib.reload(sys.modules['app'])
        if 'config' in sys.modules:
            importlib.reload(sys.modules['config'])
            
        import app
        
        # Test with Flask test client
        with app.app.test_client() as client:
            response = client.get('/test-db')
            
            if response.status_code == 200:
                data = response.get_json()
                print("✅ Database connection working!")
                print(f"   Status: {data.get('database_status')}")
                
                collections = data.get('collections', {})
                for collection, count in collections.items():
                    print(f"   {collection}: {count}")
                
                return True
            else:
                data = response.get_json() if response.data else {}
                print(f"❌ Database test failed: {response.status_code}")
                print(f"   Error: {data.get('error', 'Unknown error')}")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def main():
    """Main function to fix MongoDB connection"""
    print("🔧 MONGODB CONNECTION TROUBLESHOOTER")
    print("="*60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Test basic connection
    connection_type = test_basic_connection()
    
    if not connection_type:
        print("\n❌ CANNOT FIX: No working MongoDB connection found")
        print("\nOptions:")
        print("1. Install local MongoDB: https://www.mongodb.com/try/download/community")
        print("2. Check your MongoDB Atlas credentials")
        print("3. Continue using simple mode (recommended)")
        return False
    
    print(f"\n✅ Found working connection type: {connection_type}")
    
    # Step 2: Fix config file
    if not fix_config_file(connection_type):
        print("\n❌ Failed to fix configuration")
        return False
    
    # Step 3: Update .env file
    if not update_env_file(connection_type):
        print("\n⚠️  .env update failed, but connection might still work")
    
    # Step 4: Test fixed connection
    if test_fixed_connection():
        print(f"\n🎉 SUCCESS: MongoDB connection fixed!")
        print(f"   Connection type: {connection_type}")
        print(f"   You can now use 'start_full_app.bat'")
        return True
    else:
        print(f"\n❌ Connection still not working after fixes")
        print(f"   Recommendation: Continue using simple mode")
        return False

def create_local_mongodb_config():
    """Create a config for local MongoDB setup"""
    print("\n🔧 CREATING LOCAL MONGODB CONFIGURATION")
    print("="*60)
    
    local_config = """import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # MongoDB configuration (Local)
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost:27017/smart_resume',
        'connect': False
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
"""
    
    try:
        with open('config_local.py', 'w', encoding='utf-8') as f:
            f.write(local_config)
        print("✅ Created config_local.py for local MongoDB")
        print("   To use: Copy config_local.py to config.py after installing MongoDB")
        return True
    except Exception as e:
        print(f"❌ Failed to create local config: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print(f"\n💡 CREATING ALTERNATIVE CONFIGS")
        create_local_mongodb_config()
    
    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sys.exit(0 if success else 1)
