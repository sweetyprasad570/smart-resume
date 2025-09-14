#!/usr/bin/env python3
"""
Test new MongoDB Atlas connection
"""
from pymongo import MongoClient
import sys

def test_new_atlas_connection():
    """Test new MongoDB Atlas connection"""
    print("Testing new MongoDB Atlas connection...")
    
    # New connection string from .env
    connection_string = "mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/?retryWrites=true&w=majority"
    
    try:
        # Create client with timeout
        client = MongoClient(
            connection_string,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000
        )
        
        # Test connection
        server_info = client.admin.command('ping')
        print("SUCCESS: Database connection established!")
        
        # Get database info - use smart_resume as default
        db = client['smart_resume']
        
        print(f"Database name: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"Collections found: {len(collections)}")
        
        if collections:
            for collection_name in collections:
                count = db[collection_name].count_documents({})
                print(f"  - {collection_name}: {count} documents")
        else:
            print("  No collections found (new database)")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"FAILED: Connection error - {str(e)}")
        return False

if __name__ == "__main__":
    success = test_new_atlas_connection()
    sys.exit(0 if success else 1)
