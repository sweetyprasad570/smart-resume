#!/usr/bin/env python3
"""
MongoDB Atlas Connection Fix Tester
Tests multiple connection strategies to resolve SSL issues
"""

import sys
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure, OperationFailure
import ssl
import certifi

def test_connection(config_name, connection_params):
    """Test a MongoDB connection with given parameters"""
    print(f"\n🔍 Testing {config_name}...")
    print(f"📡 Connection string: {connection_params['host'][:80]}...")
    
    try:
        # Create client with parameters
        client = MongoClient(**connection_params)
        
        # Test the connection
        print("⏳ Attempting connection...")
        client.admin.command('ping')
        
        # Test database operations
        db = client.get_default_database() or client.smart_resume
        collections = db.list_collection_names()
        
        print(f"✅ {config_name} - CONNECTION SUCCESSFUL!")
        print(f"📊 Database: {db.name}")
        print(f"📁 Collections: {len(collections)} found")
        if collections:
            print(f"   Collections: {', '.join(collections[:3])}")
        
        # Close connection
        client.close()
        return True
        
    except ServerSelectionTimeoutError as e:
        print(f"❌ {config_name} - Timeout: {str(e)[:100]}...")
        return False
    except ConnectionFailure as e:
        print(f"❌ {config_name} - Connection failed: {str(e)[:100]}...")
        return False
    except OperationFailure as e:
        print(f"❌ {config_name} - Authentication failed: {str(e)[:100]}...")
        return False
    except Exception as e:
        print(f"❌ {config_name} - Unexpected error: {str(e)[:100]}...")
        return False

def main():
    print("🚀 MongoDB Atlas SSL Fix Tester")
    print("=" * 50)
    
    # Test strategies in order of preference
    strategies = [
        {
            "name": "Strategy 1: SSL Disabled",
            "params": {
                'host': 'mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/smart_resume?ssl=false&retryWrites=true&w=majority',
                'serverSelectionTimeoutMS': 10000,
                'socketTimeoutMS': 10000,
                'connectTimeoutMS': 10000
            }
        },
        {
            "name": "Strategy 2: SSL with Certificate Bypass", 
            "params": {
                'host': 'mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/smart_resume?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority&tlsAllowInvalidCertificates=true&tlsInsecure=true',
                'serverSelectionTimeoutMS': 10000,
                'ssl': True,
                'ssl_cert_reqs': ssl.CERT_NONE,
                'tlsAllowInvalidCertificates': True
            }
        },
        {
            "name": "Strategy 3: Alternative Atlas Connection",
            "params": {
                'host': 'mongodb+srv://sweetykp23hcs_db_user:2023HC0570@smart-resume-jobmatch.iewebgp.mongodb.net/smart_resume?ssl=false&retryWrites=true&w=majority',
                'serverSelectionTimeoutMS': 10000,
                'socketTimeoutMS': 10000,
                'connectTimeoutMS': 10000
            }
        },
        {
            "name": "Strategy 4: SSL with certifi CA Bundle",
            "params": {
                'host': 'mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/smart_resume?retryWrites=true&w=majority',
                'serverSelectionTimeoutMS': 10000,
                'ssl': True,
                'ssl_ca_certs': certifi.where(),
                'tlsAllowInvalidHostnames': True
            }
        }
    ]
    
    successful_strategies = []
    
    # Test each strategy
    for strategy in strategies:
        success = test_connection(strategy["name"], strategy["params"])
        if success:
            successful_strategies.append(strategy)
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS")
    print("=" * 50)
    
    if successful_strategies:
        print(f"✅ Found {len(successful_strategies)} working connection(s)!")
        print("\n🎯 RECOMMENDED SOLUTION:")
        best_strategy = successful_strategies[0]
        print(f"   {best_strategy['name']}")
        
        print(f"\n📝 To apply this fix:")
        print(f"1. Backup your current config.py")
        print(f"2. Copy config_atlas_fixed.py to config.py")
        print(f"3. The working strategy is already set as default")
        
        # Create a working config file
        print(f"\n🔧 Creating working configuration...")
        try:
            with open('config_working.py', 'w') as f:
                f.write(f"""import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Working MongoDB configuration - {best_strategy['name']}
    MONGODB_SETTINGS = {best_strategy['params']}

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-key-for-smart-resume'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['cookies']

    # File upload configuration
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {{'png', 'jpg', 'jpeg', 'gif'}}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
""")
            print("✅ Created config_working.py with the best configuration!")
        except Exception as e:
            print(f"❌ Failed to create config file: {e}")
        
    else:
        print("❌ No working connections found!")
        print("\n🔍 TROUBLESHOOTING SUGGESTIONS:")
        print("1. Check your internet connection")
        print("2. Verify MongoDB Atlas cluster is running")
        print("3. Check Network Access settings in Atlas (whitelist 0.0.0.0/0)")
        print("4. Verify database user credentials")
        print("5. Consider using simple_app.py instead")
    
    print(f"\n🏁 Testing complete!")

if __name__ == "__main__":
    main()
