from flask import Flask
from models import db, User, Resume
from config import Config

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

with app.app_context():
    # Create tables
    db.create_all()
    print("✅ Tables created successfully!")
    
    # Test basic database operations
    try:
        # Count existing records
        user_count = User.query.count()
        resume_count = Resume.query.count()
        
        print(f"📊 Current records:")
        print(f"   Users: {user_count}")
        print(f"   Resumes: {resume_count}")
        
        # Test creating a user
        if user_count == 0:
            test_user = User(name="Test User", email="test@test.com", password="test123")
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created!")
            
            # Test creating a resume for the user
            test_resume = Resume(
                user_id=test_user.id,
                education="Test Education",
                skills="Python, Flask"
            )
            db.session.add(test_resume)
            db.session.commit()
            print("✅ Test resume created!")
            
            # Test relationship
            user_resumes = test_user.resumes
            print(f"🔗 User has {len(user_resumes)} resume(s)")
            print("✅ User-Resume relationship working!")
        
        print("\n🎉 Database is working perfectly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
