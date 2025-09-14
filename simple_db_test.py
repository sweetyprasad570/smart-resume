#!/usr/bin/env python3
"""
Simple MongoDB connection test using pymongo directly
"""
import os
import ssl
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    """Test MongoDB Atlas connection using pymongo"""
    print("🔍 Testing MongoDB Atlas connection...")
    
    # Connection string from config
    connection_string = "mongodb+srv://crohitcsr23hcs:Rohit021512@cluster0.snmtjuv.mongodb.net/?retryWrites=true&w=majority"
    
    # Try multiple connection configurations
    connection_configs = [
        {
            "name": "Standard SSL",
            "params": {
                "serverSelectionTimeoutMS": 10000,
                "connectTimeoutMS": 10000,
                "socketTimeoutMS": 10000,
                "tls": True,
                "tlsAllowInvalidCertificates": True
            }
        },
        {
            "name": "Relaxed SSL",
            "params": {
                "serverSelectionTimeoutMS": 15000,
                "connectTimeoutMS": 15000,
                "socketTimeoutMS": 15000,
                "ssl": True,
                "ssl_cert_reqs": ssl.CERT_NONE,
                "ssl_match_hostname": False
            }
        },
        {
            "name": "No SSL Verification",
            "params": {
                "serverSelectionTimeoutMS": 20000,
                "connectTimeoutMS": 20000,
                "socketTimeoutMS": 20000,
                "tls": True,
                "tlsInsecure": True
            }
        }
    ]
    
    for config in connection_configs:
        print(f"\n🔧 Trying {config['name']} configuration...")
        
        try:
            # Create MongoDB client
            client = MongoClient(connection_string, **config['params'])
        
            # Test the connection
            server_info = client.admin.command('ismaster')
            
            print("✅ Database connection successful!")
            print(f"📊 Connected to: {server_info.get('me', 'MongoDB Atlas')}")
            
            # Get database info
            db = client.get_default_database()
            if db is None:
                # Use a default database name
                db = client['smart_resume']
            
            print(f"🗄️  Database name: {db.name}")
            
            # List collections
            collections = db.list_collection_names()
            print(f"📋 Collections: {collections if collections else 'No collections found'}")
            
            # Get collection stats
            for collection_name in collections:
                collection = db[collection_name]
                count = collection.count_documents({})
                print(f"   📄 {collection_name}: {count} documents")
            
            client.close()
            return True
            
        except Exception as e:
            print(f"❌ {config['name']} failed: {str(e)}")
            continue
    
    # If all configurations failed
    print(f"\n💥 All connection attempts failed!")
    print(f"\n💡 Troubleshooting tips:")
    print(f"   • Check network connectivity")
    print(f"   • Verify MongoDB Atlas cluster is running")
    print(f"   • Check IP whitelist in MongoDB Atlas")
    print(f"   • Verify connection string credentials")
    print(f"   • Try connecting from MongoDB Compass")
    
    return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    if success:
        print("\n🎉 Database is connected and ready!")
    else:
        print("\n💥 Database connection issues detected!")
