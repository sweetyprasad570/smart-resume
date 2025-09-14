#!/usr/bin/env python3
"""
Comprehensive MongoDB Atlas connection diagnostics
"""
import pymongo
import socket
import ssl
import urllib.parse
from pymongo import MongoClient
import dns.resolver
import requests

def test_internet_connectivity():
    """Test basic internet connectivity"""
    print("🌐 Testing internet connectivity...")
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            print("   ✅ Internet connection working")
            return True
    except:
        print("   ❌ No internet connection")
        return False

def test_dns_resolution():
    """Test DNS resolution for MongoDB Atlas"""
    print("🔍 Testing DNS resolution...")
    try:
        hostname = "cluster0.xs5k84y.mongodb.net"
        ip_address = socket.gethostbyname(hostname)
        print(f"   ✅ {hostname} resolves to {ip_address}")
        return True
    except Exception as e:
        print(f"   ❌ DNS resolution failed: {str(e)}")
        return False

def test_port_connectivity():
    """Test port connectivity to MongoDB Atlas"""
    print("🔌 Testing port connectivity...")
    hostname = "cluster0.xs5k84y.mongodb.net"
    port = 27017
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((hostname, port))
        sock.close()
        
        if result == 0:
            print(f"   ✅ Port {port} is accessible")
            return True
        else:
            print(f"   ❌ Port {port} is blocked or unreachable")
            return False
    except Exception as e:
        print(f"   ❌ Port test failed: {str(e)}")
        return False

def test_ssl_connectivity():
    """Test SSL connectivity to MongoDB Atlas"""
    print("🔒 Testing SSL connectivity...")
    hostname = "cluster0.xs5k84y.mongodb.net"
    port = 27017
    
    try:
        # Create SSL context
        context = ssl.create_default_context()
        
        # Test SSL connection
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print(f"   ✅ SSL handshake successful")
                print(f"   🔐 SSL version: {ssock.version()}")
                return True
    except Exception as e:
        print(f"   ❌ SSL connection failed: {str(e)}")
        return False

def test_mongodb_connection_simple():
    """Test simple MongoDB connection without SSL complications"""
    print("📊 Testing simple MongoDB connection...")
    
    # Try different connection string variations
    connection_strings = [
        # Original
        "mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/smart_resume?retryWrites=true&w=majority",
        
        # With SSL disabled
        "mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/smart_resume?retryWrites=true&w=majority&ssl=false",
        
        # With SSL cert check disabled
        "mongodb+srv://prasadsweety1611_db_user:sweety123@cluster0.xs5k84y.mongodb.net/smart_resume?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE",
        
        # Direct connection (no SRV)
        "mongodb://prasadsweety1611_db_user:sweety123@cluster0-shard-00-00.xs5k84y.mongodb.net:27017,cluster0-shard-00-01.xs5k84y.mongodb.net:27017,cluster0-shard-00-02.xs5k84y.mongodb.net:27017/smart_resume?ssl=true&replicaSet=atlas-123abc-shard-0&authSource=admin&retryWrites=true&w=majority"
    ]
    
    for i, conn_str in enumerate(connection_strings, 1):
        print(f"\n   🔄 Testing connection method {i}/4...")
        try:
            client = MongoClient(conn_str, serverSelectionTimeoutMS=8000)
            
            # Test connection
            server_info = client.admin.command('ping')
            print(f"   ✅ Connection method {i} successful!")
            
            # Get server info
            info = client.server_info()
            print(f"   📊 Server version: {info.get('version')}")
            
            client.close()
            return True
            
        except Exception as e:
            print(f"   ❌ Connection method {i} failed: {str(e)}")
    
    return False

def check_firewall_settings():
    """Check Windows Firewall settings"""
    print("🔥 Checking firewall settings...")
    try:
        import subprocess
        result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles', 'state'], 
                               capture_output=True, text=True)
        if 'ON' in result.stdout:
            print("   ⚠️  Windows Firewall is enabled - might block MongoDB connections")
            print("   💡 Try temporarily disabling Windows Firewall for testing")
        else:
            print("   ✅ Windows Firewall appears to be off")
    except:
        print("   ❓ Could not check firewall status")

def main():
    """Run comprehensive diagnostics"""
    print("🔧 MongoDB Atlas Connection Diagnostics")
    print("=" * 50)
    
    results = {
        'internet': test_internet_connectivity(),
        'dns': test_dns_resolution(),
        'port': test_port_connectivity(),
        'ssl': test_ssl_connectivity(),
        'mongodb': test_mongodb_connection_simple()
    }
    
    check_firewall_settings()
    
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test.upper():<12}: {status}")
    
    if all(results.values()):
        print("\n🎉 All tests passed! MongoDB Atlas should be working.")
    else:
        print("\n🛠️  Issues detected. Check the failed tests above.")
        
        # Specific recommendations
        if not results['internet']:
            print("   🌐 Fix internet connection first")
        elif not results['dns']:
            print("   🔍 Check DNS settings or try different DNS server (8.8.8.8)")
        elif not results['port']:
            print("   🔌 Port 27017 is blocked - check firewall/router settings")
        elif not results['ssl']:
            print("   🔒 SSL/TLS issues - might need certificate updates")
        else:
            print("   📊 MongoDB-specific authentication or configuration issue")

if __name__ == "__main__":
    main()
