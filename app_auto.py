import os
from flask import Flask, render_template, jsonify, request, session
from flask_cors import CORS
import bcrypt
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Required for sessions
CORS(app)

# Check for MongoDB URL
MONGODB_URL = os.environ.get('DATABASE_URL') or os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URL')
USE_MONGODB = False

# Try to import and initialize MongoDB if URL is present
if MONGODB_URL:
    try:
        from flask_mongoengine import MongoEngine
        from models import User, Resume, Job
        
        # Configure MongoDB
        app.config['MONGODB_SETTINGS'] = {
            'host': MONGODB_URL,
            'connect': False,
            'ssl': True,
            'ssl_cert_reqs': None,
            'tlsAllowInvalidCertificates': True,
            'serverSelectionTimeoutMS': 10000
        }
        
        db = MongoEngine()
        db.init_app(app)
        
        # Test MongoDB connection
        with app.app_context():
            User.objects.count()  # Test query
        
        USE_MONGODB = True
        print("✅ MongoDB connection successful - using database storage")
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        print("🔄 Falling back to in-memory storage")
        USE_MONGODB = False

if not USE_MONGODB:
    print("📝 Using in-memory storage (no MongoDB URL found or connection failed)")
    # Simple in-memory storage for testing
    users = []
    resumes = []
    jobs = []

# Session management
def get_current_user_id():
    return session.get('user_id')

def is_logged_in():
    return 'user_id' in session

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/resumes')
def resumes_page():
    return render_template('resumes.html')

@app.route('/jobs')
def jobs_page():
    return render_template('jobs.html')

@app.route('/profile')
def profile_page():
    return render_template('dashboard.html')  # Using dashboard as profile for now

@app.route('/api/status')
def api_status():
    storage_mode = "MongoDB" if USE_MONGODB else "In-Memory"
    return jsonify({
        "message": "Smart Resume API is running!",
        "status": "success",
        "storage_mode": storage_mode,
        "mongodb_url_present": MONGODB_URL is not None,
        "database": "MongoDB Atlas" if USE_MONGODB else "in-memory (testing mode)",
        "endpoints": {
            "home": "/",
            "login": "/login",
            "register": "/register",
            "dashboard": "/dashboard",
            "resumes": "/resumes",
            "jobs": "/jobs",
            "api_status": "/api/status"
        }
    })

@app.route('/health')
def health():
    storage_mode = "MongoDB" if USE_MONGODB else "In-Memory"
    return jsonify({
        "status": "healthy",
        "storage_mode": storage_mode,
        "database": "MongoDB connected" if USE_MONGODB else "in-memory (testing mode)"
    })

@app.route('/test-db')
def test_db():
    if USE_MONGODB:
        try:
            from models import User, Resume, Job, PasswordReset
            
            # Check collections by counting documents
            user_count = User.objects.count()
            resume_count = Resume.objects.count()
            job_count = Job.objects.count()
            password_reset_count = PasswordReset.objects.count()

            return jsonify({
                "database_status": "working",
                "storage_mode": "MongoDB",
                "mongodb_url": MONGODB_URL[:50] + "..." if MONGODB_URL else None,
                "collections": {
                    "users": f"{user_count} documents",
                    "resumes": f"{resume_count} documents",
                    "jobs": f"{job_count} documents",
                    "password_resets": f"{password_reset_count} documents"
                },
                "message": "MongoDB database is working fine!"
            })
        except Exception as e:
            return jsonify({
                "database_status": "error",
                "storage_mode": "MongoDB",
                "error": str(e)
            }), 500
    else:
        return jsonify({
            "database_status": "working",
            "storage_mode": "In-Memory",
            "collections": {
                "users": f"{len(users)} documents",
                "resumes": f"{len(resumes)} documents",
                "jobs": f"{len(jobs)} documents"
            },
            "message": "In-memory database is working fine!"
        })

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        print(f"=== LOGIN ATTEMPT ===")
        print(f"Email: {email}")
        print(f"Storage mode: {'MongoDB' if USE_MONGODB else 'In-Memory'}")
        
        # Validate input
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400
        
        user = None
        
        if USE_MONGODB:
            from models import User
            try:
                user_obj = User.objects(email=email).first()
                if user_obj and user_obj.check_password(password):
                    user = {
                        'id': str(user_obj.id),
                        'name': user_obj.name,
                        'email': user_obj.email
                    }
            except Exception as e:
                print(f"MongoDB login error: {str(e)}")
        else:
            # In-memory storage
            print(f"Total users in system: {len(users)}")
            for u in users:
                if u['email'].lower() == email:
                    # Verify password
                    try:
                        password_bytes = password.encode('utf-8')
                        hashed_password = u['password'].encode('utf-8')
                        
                        if bcrypt.checkpw(password_bytes, hashed_password):
                            user = u
                            break
                    except Exception as password_error:
                        print(f"Password verification error: {password_error}")
        
        if user:
            # Login successful - create session
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_name'] = user['name']
            
            print(f"Login successful for user: {user['name']}")
            print(f"Session created with user_id: {user['id']}")
            print("=====================")
            
            return jsonify({
                'message': 'Login successful',
                'access_token': f'session_token_{user["id"]}',
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email']
                }
            }), 200
        else:
            print("User not found or invalid credentials")
            return jsonify({'message': 'Invalid email or password'}), 401
            
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': 'Login failed. Please try again.'}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        print(f"=== REGISTRATION ATTEMPT ===")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Storage mode: {'MongoDB' if USE_MONGODB else 'In-Memory'}")
        
        # Validate input
        if not name or not email or not password:
            return jsonify({'message': 'Name, email and password are required'}), 400
        
        if len(password) < 6:
            return jsonify({'message': 'Password must be at least 6 characters long'}), 400
        
        # Check if user already exists
        user_exists = False
        
        if USE_MONGODB:
            from models import User
            try:
                existing_user = User.objects(email=email).first()
                if existing_user:
                    user_exists = True
            except Exception as e:
                print(f"MongoDB user check error: {str(e)}")
        else:
            # In-memory storage
            for user in users:
                if user['email'].lower() == email:
                    user_exists = True
                    break
        
        if user_exists:
            print(f"User already exists with email: {email}")
            return jsonify({'message': 'User with this email already exists'}), 409
        
        # Create new user
        if USE_MONGODB:
            from models import User
            try:
                new_user = User(name=name, email=email)
                new_user.set_password(password)
                new_user.save()
                
                print(f"User registered successfully in MongoDB: {name} ({email})")
            except Exception as e:
                print(f"MongoDB user creation error: {str(e)}")
                return jsonify({'message': 'Registration failed. Please try again.'}), 500
        else:
            # In-memory storage
            try:
                password_bytes = password.encode('utf-8')
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password_bytes, salt)
                
                new_user = {
                    'id': str(uuid.uuid4()),
                    'name': name,
                    'email': email,
                    'password': hashed_password.decode('utf-8'),  # Store as string
                    'created_at': datetime.utcnow().isoformat()
                }
                
                users.append(new_user)
                print(f"User registered successfully in memory: {name} ({email})")
                print(f"Total users now: {len(users)}")
            except Exception as e:
                print(f"In-memory user creation error: {str(e)}")
                return jsonify({'message': 'Registration failed. Please try again.'}), 500
        
        print("=========================")
        
        return jsonify({
            'message': 'Registration successful! You can now login.',
            'status': 'success'
        }), 201
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({'message': 'Registration failed. Please try again.'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

# Jobs endpoints (simplified for both storage modes)
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    # Create some sample jobs for demo
    sample_jobs = []
    
    if USE_MONGODB:
        try:
            from models import Job
            jobs_data = Job.objects()
            if jobs_data.count() == 0:
                # Create sample jobs in MongoDB
                sample_jobs_data = [
                    {
                        'job_title': 'Frontend Developer',
                        'company': 'TechCorp Inc.',
                        'required_skills': ['JavaScript', 'React', 'HTML', 'CSS']
                    },
                    {
                        'job_title': 'Python Developer', 
                        'company': 'DataSoft Solutions',
                        'required_skills': ['Python', 'Django', 'PostgreSQL', 'API Development']
                    },
                    {
                        'job_title': 'Full Stack Developer',
                        'company': 'Innovation Labs', 
                        'required_skills': ['JavaScript', 'Python', 'React', 'Node.js', 'MongoDB']
                    }
                ]
                
                for job_data in sample_jobs_data:
                    job = Job(**job_data)
                    job.save()
                
                jobs_data = Job.objects()
            
            sample_jobs = []
            for job in jobs_data:
                sample_jobs.append({
                    'id': str(job.id),
                    'job_title': job.job_title,
                    'company': job.company,
                    'required_skills': job.required_skills,
                    'created_at': job.created_at.isoformat() if job.created_at else datetime.utcnow().isoformat(),
                    'updated_at': job.updated_at.isoformat() if job.updated_at else datetime.utcnow().isoformat()
                })
        except Exception as e:
            print(f"MongoDB jobs error: {str(e)}")
    else:
        # In-memory storage
        if not jobs:  # Only add sample data if jobs list is empty
            from datetime import datetime, timedelta
            
            sample_jobs_data = [
                {
                    'id': str(uuid.uuid4()),
                    'job_title': 'Frontend Developer',
                    'company': 'TechCorp Inc.',
                    'required_skills': ['JavaScript', 'React', 'HTML', 'CSS'],
                    'created_at': (datetime.utcnow() - timedelta(days=2)).isoformat(),
                    'updated_at': (datetime.utcnow() - timedelta(days=2)).isoformat()
                },
                {
                    'id': str(uuid.uuid4()),
                    'job_title': 'Python Developer',
                    'company': 'DataSoft Solutions',
                    'required_skills': ['Python', 'Django', 'PostgreSQL', 'API Development'],
                    'created_at': (datetime.utcnow() - timedelta(days=1)).isoformat(),
                    'updated_at': (datetime.utcnow() - timedelta(days=1)).isoformat()
                },
                {
                    'id': str(uuid.uuid4()),
                    'job_title': 'Full Stack Developer',
                    'company': 'Innovation Labs',
                    'required_skills': ['JavaScript', 'Python', 'React', 'Node.js', 'MongoDB'],
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
            ]
            
            jobs.extend(sample_jobs_data)
        
        sample_jobs = jobs
    
    return jsonify({'jobs': sample_jobs}), 200

@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    job = None
    
    if USE_MONGODB:
        try:
            from models import Job
            from bson import ObjectId
            job_obj = Job.objects(id=ObjectId(job_id)).first()
            if job_obj:
                job = {
                    'id': str(job_obj.id),
                    'job_title': job_obj.job_title,
                    'company': job_obj.company,
                    'required_skills': job_obj.required_skills,
                    'created_at': job_obj.created_at.isoformat() if job_obj.created_at else datetime.utcnow().isoformat(),
                    'updated_at': job_obj.updated_at.isoformat() if job_obj.updated_at else datetime.utcnow().isoformat()
                }
        except Exception as e:
            print(f"MongoDB get job error: {str(e)}")
    else:
        # In-memory storage
        job = next((j for j in jobs if j['id'] == job_id), None)
    
    if not job:
        return jsonify({'message': 'Job not found'}), 404
        
    return jsonify({'job': job}), 200

if __name__ == '__main__':
    print("Starting Smart Resume Auto-Detection Mode...")
    print(f"MongoDB URL present: {MONGODB_URL is not None}")
    print(f"Using storage mode: {'MongoDB' if USE_MONGODB else 'In-Memory'}")
    print("Access the application at: http://localhost:5000")
    print("Or from other devices at: http://0.0.0.0:5000")
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Error starting the application: {e}")
