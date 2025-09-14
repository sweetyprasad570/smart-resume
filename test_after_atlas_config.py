#!/usr/bin/env python3
"""
Test MongoDB connection after Atlas configuration changes
"""
import pymongo
from pymongo import MongoClient
import time

def test_connection_with_retry():
    """Test connection with multiple retry attempts"""
    
    connection_string = "mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/smart_resume?retryWrites=true&w=majority"
    
    print("🔍 Testing MongoDB Atlas connection after network configuration...")
    print(f"📍 Your IP: 103.90.35.114")
    print(f"🔗 Connection: cluster0.xs5k84y.mongodb.net")
    
    for attempt in range(3):
        try:
            print(f"\n🔄 Attempt {attempt + 1}/3...")
            
            client = MongoClient(connection_string, serverSelectionTimeoutMS=15000)
            
            # Test connection
            server_info = client.admin.command('ismaster')
            
            print("✅ SUCCESS! Database connection established!")
            print(f"📊 Connected to: {server_info.get('me', 'MongoDB Atlas')}")
            
            # Test database operations
            db = client['smart_resume']
            collections = db.list_collection_names()
            
            print(f"📈 Database info:")
            print(f"   📚 Collections: {collections}")
            print(f"   ✅ Database access confirmed!")
            
            client.close()
            return True
            
        except pymongo.errors.ServerSelectionTimeoutError:
            print(f"❌ Attempt {attempt + 1} failed: Connection timeout")
            if attempt < 2:
                print("⏳ Waiting 10 seconds before retry...")
                time.sleep(10)
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < 2:
                print("⏳ Waiting 10 seconds before retry...")
                time.sleep(10)
    
    print("\n💥 All connection attempts failed!")
    print("\n🔍 Troubleshooting checklist:")
    print("   ☐ IP address 103.90.35.114 is whitelisted in Atlas")
    print("   ☐ Cluster is running (not paused)")
    print("   ☐ Database user exists with correct password")
    print("   ☐ Internet connection is stable")
    
    return False

if __name__ == "__main__":
    success = test_connection_with_retry()
    if success:
        print("\n🎉 Atlas connection is now working!")
    else:
        print("\n🛠️  Please check your Atlas configuration and try again")
