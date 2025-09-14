#!/usr/bin/env python3
"""
Simple MongoDB connection test using pymongo directly
"""
import pymongo
from pymongo import MongoClient
from config import Config
import sys

def test_mongodb_connection():
    """Test MongoDB Atlas connection using pymongo directly"""
    print("🔍 Testing MongoDB Atlas connection...")
    
    try:
        # Get connection string from config
        mongo_uri = Config.MONGODB_SETTINGS['host']
        timeout_ms = Config.MONGODB_SETTINGS.get('serverSelectionTimeoutMS', 10000)
        
        # Create MongoDB client
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=timeout_ms)
        
        # Test the connection
        print("🔗 Attempting to connect...")
        server_info = client.admin.command('ismaster')
        
        print("✅ Database connection successful!")
        print(f"📊 Connected to: {server_info.get('me', 'MongoDB Atlas')}")
        
        # Get server info
        server_info_detail = client.server_info()
        print(f"🏷️  Server version: {server_info_detail.get('version', 'Unknown')}")
        
        # Test database access
        db = client['smart_resume']
        collections = db.list_collection_names()
        
        print(f"📈 Database 'smart_resume' info:")
        print(f"   📚 Collections: {collections}")
        
        # Count documents in collections if they exist
        if 'user' in collections:
            user_count = db['user'].count_documents({})
            print(f"   👥 Users: {user_count}")
        
        if 'resume' in collections:
            resume_count = db['resume'].count_documents({})
            print(f"   📄 Resumes: {resume_count}")
        
        client.close()
        return True
        
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print("❌ Database connection failed!")
        print("🔥 Error: Connection timeout - unable to reach MongoDB Atlas")
        print("💡 Check your internet connection and MongoDB Atlas network access settings")
        return False
    except pymongo.errors.ConfigurationError as e:
        print("❌ Database connection failed!")
        print(f"🔥 Configuration Error: {str(e)}")
        print("💡 Check your MongoDB connection string")
        return False
    except Exception as e:
        print("❌ Database connection failed!")
        print(f"🔥 Error: {str(e)}")
        print("💡 Check your MongoDB Atlas connection string and credentials")
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    if success:
        print("\n🎉 Database is connected and ready!")
        sys.exit(0)
    else:
        print("\n💥 Database connection issues detected!")
        sys.exit(1)
