from flask_mongoengine import MongoEngine
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime, timedelta
import bcrypt

db = MongoEngine()

class User(db.Document):
    name = db.StringField(required=True, max_length=100)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, max_length=255)
    is_admin = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.utcnow)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def generate_tokens(self):
        access_token = create_access_token(identity=str(self.id))
        refresh_token = create_refresh_token(identity=str(self.id))
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

class Resume(db.Document):
    user = db.ReferenceField(User, required=True)
    
    # Personal Information Fields
    full_name = db.StringField(max_length=100)
    email = db.EmailField()
    phone = db.StringField(max_length=20)
    linkedin = db.URLField()
    address = db.StringField(max_length=200)
    summary = db.StringField(max_length=1000)  # Professional summary
    
    # Resume Sections
    education = db.StringField()
    experience = db.StringField()
    projects = db.StringField()
    skills = db.StringField()
    skill_ratings = db.DictField()  # Store as dict
    
    # Additional Fields
    profile_picture = db.StringField(max_length=255)
    template_type = db.StringField(default='modern', choices=['modern', 'classic', 'creative', 'minimal'])
    is_public = db.BooleanField(default=False)
    
    # Timestamps
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        super(Resume, self).save(*args, **kwargs)

class Job(db.Document):
    job_title = db.StringField(required=True, max_length=100)
    company = db.StringField(required=True, max_length=100)
    required_skills = db.ListField(db.StringField())  # Store as list of strings
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)

class PasswordReset(db.Document):
    user = db.ReferenceField(User, required=True)
    otp = db.StringField(required=True, max_length=6)
    expiry = db.DateTimeField(required=True)
    created_at = db.DateTimeField(default=datetime.utcnow)

    def is_valid(self):
        return datetime.utcnow() < self.expiry
