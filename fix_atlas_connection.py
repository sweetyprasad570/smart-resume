#!/usr/bin/env python3
"""
MongoDB Atlas Connection Fixer - Specifically for Atlas SSL issues
"""

import os
from dotenv import load_dotenv

def fix_atlas_connection():
    """Fix MongoDB Atlas connection with proper SSL settings"""
    
    load_dotenv()
    current_url = os.getenv('DATABASE_URL', '')
    
    print("🔧 MONGODB ATLAS CONNECTION FIXER")
    print("="*60)
    print(f"Current DATABASE_URL: {current_url[:50]}...")
    
    if not current_url or 'mongodb+srv://' not in current_url:
        print("❌ No valid MongoDB Atlas URL found in .env file")
        return False
    
    # Extract connection details
    try:
        # Parse the URL to add SSL parameters
        if '?' in current_url:
            base_url, params = current_url.split('?', 1)
        else:
            base_url = current_url
            params = ""
        
        # Add SSL bypass parameters
        ssl_params = [
            "ssl=true",
            "ssl_cert_reqs=CERT_NONE", 
            "retryWrites=true",
            "w=majority",
            "tlsAllowInvalidCertificates=true"
        ]
        
        if params:
            fixed_url = f"{base_url}?{params}&{'&'.join(ssl_params)}"
        else:
            fixed_url = f"{base_url}?{'&'.join(ssl_params)}"
        
        print(f"✅ Generated fixed URL with SSL bypass")
        
        # Create updated config.py
        config_content = f'''import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # MongoDB configuration (Atlas with SSL bypass)
    MONGODB_SETTINGS = {{
        'host': '{fixed_url}',
        'connect': False,
        'ssl': True,
        'ssl_cert_reqs': None,
        'tlsAllowInvalidCertificates': True,
        'serverSelectionTimeoutMS': 10000
    }}

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-key-for-smart-resume'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['cookies']

    # File upload configuration
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {{'png', 'jpg', 'jpeg', 'gif'}}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
'''
        
        # Backup current config
        if os.path.exists('config.py'):
            with open('config_backup_atlas.py', 'w') as f:
                with open('config.py', 'r') as orig:
                    f.write(orig.read())
            print("✅ Backup created: config_backup_atlas.py")
        
        # Write new config
        with open('config.py', 'w') as f:
            f.write(config_content)
        
        print("✅ Updated config.py with Atlas SSL bypass settings")
        
        # Test the connection
        try:
            import pymongo
            client = pymongo.MongoClient(
                fixed_url,
                serverSelectionTimeoutMS=10000,
                ssl=True,
                ssl_cert_reqs=None,
                tlsAllowInvalidCertificates=True
            )
            
            # Test connection
            client.admin.command('hello')
            print("✅ Atlas connection test successful!")
            
            # Test database operations
            db = client.smart_resume
            test_collection = db.test_collection
            
            # Insert a test document
            test_doc = {"test": "connection", "timestamp": "now"}
            result = test_collection.insert_one(test_doc)
            print(f"✅ Database write test successful: {result.inserted_id}")
            
            # Clean up test document
            test_collection.delete_one({"_id": result.inserted_id})
            print("✅ Database cleanup successful")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection test failed: {str(e)[:150]}...")
            
            # Try alternative connection method
            try:
                print("🔄 Trying alternative connection method...")
                
                # Use connection string without explicit SSL params in code
                simple_client = pymongo.MongoClient(
                    base_url + "?ssl=false&retryWrites=true&w=majority",
                    serverSelectionTimeoutMS=15000
                )
                simple_client.admin.command('hello')
                print("✅ Alternative connection (SSL disabled) works!")
                
                # Update config with SSL disabled
                alt_config = config_content.replace(
                    f"'host': '{fixed_url}'",
                    f"'host': '{base_url}?ssl=false&retryWrites=true&w=majority'"
                ).replace(
                    "'ssl': True,\n        'ssl_cert_reqs': None,\n        'tlsAllowInvalidCertificates': True,",
                    "'connect': False"
                )
                
                with open('config.py', 'w') as f:
                    f.write(alt_config)
                
                print("✅ Updated config with SSL disabled (alternative method)")
                return True
                
            except Exception as e2:
                print(f"❌ Alternative method also failed: {str(e2)[:100]}...")
                return False
        
    except Exception as e:
        print(f"❌ Error processing Atlas URL: {e}")
        return False

def create_manual_atlas_config():
    """Create a manual config template for Atlas"""
    
    manual_config = '''import os
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
'''

    with open('config_atlas_manual.py', 'w') as f:
        f.write(manual_config)
    
    print("✅ Created config_atlas_manual.py")
    print("   Edit this file with your Atlas credentials and copy to config.py")

if __name__ == "__main__":
    success = fix_atlas_connection()
    
    if not success:
        print("\n💡 CREATING MANUAL CONFIGURATION TEMPLATE")
        create_manual_atlas_config()
        print("\n📝 MANUAL STEPS TO FIX ATLAS CONNECTION:")
        print("1. Check your MongoDB Atlas cluster is running")
        print("2. Verify your IP address is whitelisted in Atlas")  
        print("3. Confirm username/password are correct")
        print("4. Edit config_atlas_manual.py with correct credentials")
        print("5. Copy config_atlas_manual.py to config.py")
    else:
        print("\n🎉 SUCCESS: MongoDB Atlas connection should now work!")
        print("   Try running: start_full_app.bat")
