#!/usr/bin/env python3
"""
Database initialization script for Smart Resume application
"""
from app import create_app
from models import db, User, Resume, Job, PasswordReset
from sqlalchemy import inspect

def init_database():
    """Initialize database and create all tables"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate (for fresh start)
        db.drop_all()
        db.create_all()
        
        print("✅ Database tables created successfully!")
        
        # Test table creation by checking if they exist
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Created tables: {tables}")
        
        return True

def test_user_resume_relationship():
    """Test the user-resume relationship"""
    app = create_app()
    
    with app.app_context():
        try:
            # Create a test user
            test_user = User(
                name="John Doe", 
                email="john@example.com", 
                password="password123"
            )
            db.session.add(test_user)
            db.session.commit()
            
            # Create a resume for the user
            test_resume = Resume(
                user_id=test_user.id,
                education="B.Tech Computer Science",
                experience="2 years Python Developer",
                projects="E-commerce website, Chat application",
                skills="Python, Flask, SQLAlchemy, JavaScript",
                skill_ratings='{"Python": 8, "Flask": 7, "JavaScript": 6}'
            )
            db.session.add(test_resume)
            db.session.commit()
            
            # Test relationship
            user_resumes = test_user.resumes
            resume_owner = test_resume.user
            
            print("✅ User-Resume relationship test passed!")
            print(f"👤 User: {test_user.name} ({test_user.email})")
            print(f"📄 Resume count: {len(user_resumes)}")
            print(f"🔗 Resume owner: {resume_owner.name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Relationship test failed: {str(e)}")
            return False

def show_database_status():
    """Show current database status"""
    app = create_app()
    
    with app.app_context():
        try:
            user_count = User.query.count()
            resume_count = Resume.query.count()
            job_count = Job.query.count()
            password_reset_count = PasswordReset.query.count()
            
            print("\n📊 Database Status:")
            print(f"   Users: {user_count}")
            print(f"   Resumes: {resume_count}")
            print(f"   Jobs: {job_count}")
            print(f"   Password Resets: {password_reset_count}")
            
        except Exception as e:
            print(f"❌ Error checking database status: {str(e)}")

if __name__ == "__main__":
    print("🚀 Initializing Smart Resume Database...")
    
    # Initialize database
    if init_database():
        print("\n🧪 Testing user-resume relationship...")
        test_user_resume_relationship()
        
        print("\n📈 Checking final database status...")
        show_database_status()
        
        print("\n✨ Database integration completed successfully!")
        print("🌐 You can now run 'python app.py' to start the Flask server")
    else:
        print("❌ Database initialization failed!")
