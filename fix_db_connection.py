#!/usr/bin/env python3
"""
MongoDB Atlas Connection Fixer
Diagnoses and fixes common connection issues
"""
import os
import ssl
import socket
import requests
from pymongo import MongoClient
from urllib.parse import urlparse

def get_public_ip():
    """Get current public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        try:
            response = requests.get('https://httpbin.org/ip', timeout=5)
            return response.json()['origin']
        except:
            return "Unable to determine"

def test_dns_resolution():
    """Test DNS resolution for MongoDB Atlas"""
    hostname = "cluster0.snmtjuv.mongodb.net"
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✅ DNS Resolution: {hostname} -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ DNS Resolution failed: {e}")
        return False

def test_port_connectivity():
    """Test port 27017 connectivity"""
    hostname = "cluster0.snmtjuv.mongodb.net"
    port = 27017
    
    try:
        sock = socket.create_connection((hostname, port), timeout=10)
        sock.close()
        print(f"✅ Port {port} is accessible")
        return True
    except socket.error as e:
        print(f"❌ Port {port} connection failed: {e}")
        return False

def test_simple_connection():
    """Test with minimal connection parameters"""
    connection_strings = [
        # Simplified connection string
        "mongodb+srv://crohitcsr23hcs:Rohit021512@cluster0.snmtjuv.mongodb.net/test",
        # With specific database
        "mongodb+srv://crohitcsr23hcs:Rohit021512@cluster0.snmtjuv.mongodb.net/smart_resume",
        # With SSL disabled (not recommended for production)
        "mongodb+srv://crohitcsr23hcs:Rohit021512@cluster0.snmtjuv.mongodb.net/test?ssl=false"
    ]
    
    for i, conn_str in enumerate(connection_strings, 1):
        print(f"\n🔧 Testing connection string {i}...")
        try:
            client = MongoClient(
                conn_str,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Test connection
            client.admin.command('ping')
            print("✅ Connection successful!")
            
            # Get database info
            db_name = client.get_default_database().name if client.get_default_database() else 'test'
            db = client[db_name]
            collections = db.list_collection_names()
            
            print(f"📊 Database: {db_name}")
            print(f"📋 Collections: {collections}")
            
            client.close()
            return True
            
        except Exception as e:
            print(f"❌ Failed: {str(e)[:100]}...")
    
    return False

def main():
    """Main diagnostic function"""
    print("🔍 MongoDB Atlas Connection Diagnostics")
    print("=" * 50)
    
    # Step 1: Check public IP
    print(f"\n1️⃣ Your public IP: {get_public_ip()}")
    print("   💡 Add this IP to MongoDB Atlas Network Access whitelist")
    
    # Step 2: Test DNS resolution
    print(f"\n2️⃣ Testing DNS resolution...")
    dns_ok = test_dns_resolution()
    
    # Step 3: Test port connectivity
    print(f"\n3️⃣ Testing port connectivity...")
    port_ok = test_port_connectivity()
    
    # Step 4: Test simple connections
    print(f"\n4️⃣ Testing MongoDB connections...")
    conn_ok = test_simple_connection()
    
    # Summary and recommendations
    print(f"\n" + "=" * 50)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    if conn_ok:
        print("🎉 Database connection is working!")
    else:
        print("❌ Database connection failed")
        print("\n🔧 RECOMMENDED FIXES:")
        
        if not dns_ok:
            print("   • Check internet connection")
            print("   • Try different DNS servers (8.8.8.8, 1.1.1.1)")
        
        if not port_ok:
            print("   • Check firewall settings")
            print("   • Contact network administrator")
        
        print("   • Add your IP to MongoDB Atlas Network Access:")
        print("     1. Go to MongoDB Atlas Dashboard")
        print("     2. Navigate to Network Access")
        print("     3. Click 'Add IP Address'")
        print(f"     4. Add: {get_public_ip()}")
        print("   • Verify cluster is running (not paused)")
        print("   • Check username/password in connection string")

if __name__ == "__main__":
    main()
