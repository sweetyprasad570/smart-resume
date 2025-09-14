#!/usr/bin/env python3
"""
Simple MongoDB Atlas Diagnosis
Identifies the root cause of connection issues
"""

import socket
import ssl
from pymongo import MongoClient
from urllib.parse import urlparse
import dns.resolver
import requests

def check_internet_connectivity():
    """Check basic internet connectivity"""
    print("🌐 Testing internet connectivity...")
    try:
        response = requests.get("https://www.google.com", timeout=5)
        print("✅ Internet connection: OK")
        return True
    except Exception as e:
        print(f"❌ Internet connection: FAILED - {e}")
        return False

def check_dns_resolution():
    """Check if MongoDB cluster domains can be resolved"""
    print("\n🔍 Testing DNS resolution...")
    clusters = [
        "cluster0.xs5k84y.mongodb.net",
        "smart-resume-jobmatch.iewebgp.mongodb.net"
    ]
    
    for cluster in clusters:
        try:
            answers = dns.resolver.resolve(cluster, 'A')
            print(f"✅ DNS {cluster}: OK ({answers[0]})")
        except Exception as e:
            print(f"❌ DNS {cluster}: FAILED - {e}")

def check_mongodb_port():
    """Check if MongoDB port is accessible"""
    print("\n🔗 Testing MongoDB port accessibility...")
    hosts = [
        ("cluster0-shard-00-00.xs5k84y.mongodb.net", 27017),
        ("cluster0-shard-00-01.xs5k84y.mongodb.net", 27017),
        ("cluster0-shard-00-02.xs5k84y.mongodb.net", 27017)
    ]
    
    for host, port in hosts:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✅ Port {host}:{port}: ACCESSIBLE")
            else:
                print(f"❌ Port {host}:{port}: BLOCKED")
        except Exception as e:
            print(f"❌ Port {host}:{port}: ERROR - {e}")

def test_simplified_connection():
    """Test with the most basic connection possible"""
    print("\n🧪 Testing simplified MongoDB connection...")
    
    connection_strings = [
        # Most basic connection string
        "mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/?retryWrites=true&w=majority",
        # Alternative cluster
        "mongodb+srv://sweetykp23hcs_db_user:2023HC0570@smart-resume-jobmatch.iewebgp.mongodb.net/?retryWrites=true&w=majority"
    ]
    
    for i, conn_str in enumerate(connection_strings, 1):
        print(f"\n   Testing Connection {i}...")
        try:
            client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            print(f"   ✅ Connection {i}: SUCCESS!")
            
            # Get database info
            db = client.get_default_database()
            if db:
                collections = db.list_collection_names()
                print(f"   📊 Database: {db.name} ({len(collections)} collections)")
            
            client.close()
            return conn_str
            
        except Exception as e:
            print(f"   ❌ Connection {i}: FAILED - {str(e)[:100]}...")
    
    return None

def main():
    print("🔧 MongoDB Atlas Connection Diagnosis")
    print("=" * 45)
    
    # Step 1: Check internet
    if not check_internet_connectivity():
        print("\n💡 SOLUTION: Check your internet connection and try again.")
        return
    
    # Step 2: Check DNS
    check_dns_resolution()
    
    # Step 3: Check port access
    check_mongodb_port()
    
    # Step 4: Test actual connection
    working_connection = test_simplified_connection()
    
    print("\n" + "=" * 45)
    print("📋 DIAGNOSIS SUMMARY")
    print("=" * 45)
    
    if working_connection:
        print("✅ SOLUTION FOUND!")
        print(f"🔗 Working connection string: {working_connection}")
        
        # Create a working config
        try:
            with open('config_working_simple.py', 'w') as f:
                f.write(f'''import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Working MongoDB configuration
    MONGODB_SETTINGS = {{
        'host': '{working_connection}',
        'serverSelectionTimeoutMS': 30000,
        'socketTimeoutMS': 20000,
        'connectTimeoutMS': 20000
    }}

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-key-for-smart-resume'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['cookies']

    # File upload configuration
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {{'png', 'jpg', 'jpeg', 'gif'}}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
''')
            print("💾 Created config_working_simple.py")
            print("\n📝 To use this fix:")
            print("1. Backup: copy config.py config_backup.py")
            print("2. Apply:  copy config_working_simple.py config.py")
            print("3. Test:   python test_db_connection.py")
            
        except Exception as e:
            print(f"❌ Failed to create config: {e}")
    else:
        print("❌ NO WORKING CONNECTIONS FOUND")
        print("\n💡 LIKELY CAUSES:")
        print("1. 🔥 MongoDB Atlas clusters may be PAUSED")
        print("2. 🌐 Network Access not configured (IP whitelist)")
        print("3. 🔑 Database credentials are incorrect")
        print("4. 🏢 Corporate firewall blocking MongoDB ports")
        
        print("\n🛠️ RECOMMENDED ACTIONS:")
        print("1. Check MongoDB Atlas Dashboard:")
        print("   - Verify clusters are RUNNING (not paused)")
        print("   - Add 0.0.0.0/0 to Network Access whitelist")
        print("   - Verify database user credentials")
        print("2. Use Simple Mode: start_smart_resume.bat")
        print("3. Consider Local MongoDB installation")

if __name__ == "__main__":
    main()
