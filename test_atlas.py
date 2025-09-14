#!/usr/bin/env python3
"""
Simple Atlas connection test without Unicode
"""
from pymongo import MongoClient
import sys

def test_atlas_connection():
    """Test MongoDB Atlas connection"""
    print("Testing MongoDB Atlas connection...")
    
    connection_string = "mongodb+srv://crohitcsr23hcs:Rohit021512@cluster0.snmtjuv.mongodb.net/?retryWrites=true&w=majority"
    
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
        
        # Get database info
        db = client.get_default_database()
        if db is None:
            db = client['smart_resume']
        
        print(f"Database name: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"Collections found: {len(collections)}")
        
        for collection_name in collections:
            count = db[collection_name].count_documents({})
            print(f"  - {collection_name}: {count} documents")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"FAILED: Connection error - {str(e)}")
        return False

if __name__ == "__main__":
    success = test_atlas_connection()
    sys.exit(0 if success else 1)
