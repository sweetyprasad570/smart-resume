#!/usr/bin/env python3
"""
Test the full Flask application with MongoDB Atlas connection
"""

try:
    print("🔄 Loading Flask app with MongoDB...")
    from app import app
    
    print("✅ Flask app loaded successfully!")
    
    # Test the /test-db endpoint
    with app.test_client() as client:
        print("🧪 Testing database endpoint...")
        response = client.get('/test-db')
        
        if response.status_code == 200:
            data = response.get_json()
            print("✅ Database test successful!")
            print(f"📊 Status: {data.get('database_status')}")
            print(f"📁 Collections: {data.get('collections', {})}")
        else:
            print(f"❌ Database test failed: {response.status_code}")
            
    print("🎉 Full application test completed!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("💡 Make sure all dependencies are installed")
