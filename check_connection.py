#!/usr/bin/env python3
"""
Simple database connection test for Smart Resume app
"""
import os
from flask import Flask
from flask_mongoengine import MongoEngine
from config import Config

def test_database_connection():
    """Test MongoDB Atlas connection"""
    print("🔍 Testing MongoDB Atlas connection...")
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize MongoEngine
    db = MongoEngine()
    
    try:
        # Initialize database with app
        db.init_app(app)
        
        with app.app_context():
            # Try to connect and get server info
            from mongoengine import connect
            from mongoengine.connection import get_connection
            
            # Get the default connection
            connection = get_connection()
            
            # Test the connection by getting server info
            server_info = connection.admin.command('ismaster')
            
            print("✅ Database connection successful!")
            print(f"📊 Connected to: {server_info.get('me', 'MongoDB Atlas')}")
            print(f"🏷️  Server version: {connection.server_info().get('version', 'Unknown')}")
            
            # Test basic operations
            from models import User, Resume
            
            # Count documents
            user_count = User.objects.count()
            resume_count = Resume.objects.count()
            
            print(f"📈 Database statistics:")
            print(f"   👥 Users: {user_count}")
            print(f"   📄 Resumes: {resume_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed!")
        print(f"🔥 Error: {str(e)}")
        print(f"💡 Check your MongoDB Atlas connection string and network access")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n🎉 Database is connected and ready!")
    else:
        print("\n💥 Database connection issues detected!")
