from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simple in-memory storage for testing
users = []
resumes = []
jobs = []

# Simple session for demo (normally would use proper authentication)
current_user_id = 1

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
    return jsonify({
        "message": "Smart Resume API is running!",
        "status": "success",
        "database": "in-memory (testing mode)",
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
    return jsonify({
        "status": "healthy",
        "database": "in-memory (testing mode)"
    })

@app.route('/test-db')
def test_db():
    return jsonify({
        "database_status": "working",
        "mode": "in-memory testing",
        "collections": {
            "users": f"{len(users)} documents",
            "resumes": f"{len(resumes)} documents",
            "jobs": f"{len(jobs)} documents"
        },
        "message": "In-memory database is working fine!"
    })

# API endpoints for testing
@app.route('/api/auth/login', methods=['POST'])
def login():
    return jsonify({
        "message": "Login successful (demo mode)",
        "access_token": "demo_token_123",
        "refresh_token": "demo_refresh_456",
        "user": {
            "id": current_user_id,
            "name": "Demo User",
            "email": "demo@example.com"
        }
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    return jsonify({
        "message": "Registration successful (demo mode)",
        "status": "success"
    })

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    return jsonify({
        "message": "Logout successful (demo mode)",
        "status": "success"
    })

# Resume endpoints
@app.route('/api/resumes', methods=['POST'])
def create_resume():
    import uuid
    from datetime import datetime
    
    try:
        data = request.get_json()
        
        new_resume = {
            'id': str(uuid.uuid4()),
            'user_id': current_user_id,
            'education': data.get('education', ''),
            'experience': data.get('experience', ''),
            'projects': data.get('projects', ''),
            'skills': data.get('skills', ''),
            'skill_ratings': data.get('skill_ratings', {}),
            'profile_picture': data.get('profile_picture', ''),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        resumes.append(new_resume)
        
        return jsonify({
            'message': 'Resume created successfully!',
            'resume_id': new_resume['id']
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Error creating resume: {str(e)}'}), 500

@app.route('/api/resumes', methods=['GET'])
def get_resumes():
    user_resumes = [resume for resume in resumes if resume['user_id'] == current_user_id]
    return jsonify({'resumes': user_resumes}), 200

@app.route('/api/resumes/<resume_id>', methods=['GET'])
def get_resume(resume_id):
    resume = next((r for r in resumes if r['id'] == resume_id and r['user_id'] == current_user_id), None)
    
    if not resume:
        return jsonify({'message': 'Resume not found'}), 404
        
    return jsonify({'resume': resume}), 200

@app.route('/api/resumes/<resume_id>', methods=['PUT'])
def update_resume(resume_id):
    from datetime import datetime
    
    resume = next((r for r in resumes if r['id'] == resume_id and r['user_id'] == current_user_id), None)
    
    if not resume:
        return jsonify({'message': 'Resume not found'}), 404
    
    try:
        data = request.get_json()
        
        # Update fields if provided
        for field in ['education', 'experience', 'projects', 'skills', 'skill_ratings', 'profile_picture']:
            if field in data:
                resume[field] = data[field]
        
        resume['updated_at'] = datetime.utcnow().isoformat()
        
        return jsonify({'message': 'Resume updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error updating resume: {str(e)}'}), 500

@app.route('/api/resumes/<resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    global resumes
    
    resume = next((r for r in resumes if r['id'] == resume_id and r['user_id'] == current_user_id), None)
    
    if not resume:
        return jsonify({'message': 'Resume not found'}), 404
    
    resumes = [r for r in resumes if not (r['id'] == resume_id and r['user_id'] == current_user_id)]
    
    return jsonify({'message': 'Resume deleted successfully'}), 200

# Jobs endpoints
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    # Create some sample jobs for demo
    if not jobs:  # Only add sample data if jobs list is empty
        import uuid
        from datetime import datetime, timedelta
        
        sample_jobs = [
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
            },
            {
                'id': str(uuid.uuid4()),
                'job_title': 'DevOps Engineer',
                'company': 'CloudTech Systems',
                'required_skills': ['Docker', 'Kubernetes', 'AWS', 'Python', 'Linux'],
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'job_title': 'Data Scientist',
                'company': 'AI Innovations',
                'required_skills': ['Python', 'Machine Learning', 'Pandas', 'Scikit-learn', 'SQL'],
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
        ]
        
        jobs.extend(sample_jobs)
    
    return jsonify({'jobs': jobs}), 200

@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    job = next((j for j in jobs if j['id'] == job_id), None)
    
    if not job:
        return jsonify({'message': 'Job not found'}), 404
        
    return jsonify({'job': job}), 200

@app.route('/api/jobs', methods=['POST'])
def create_job():
    import uuid
    from datetime import datetime
    
    try:
        data = request.get_json()
        
        new_job = {
            'id': str(uuid.uuid4()),
            'job_title': data.get('job_title', ''),
            'company': data.get('company', ''),
            'required_skills': data.get('required_skills', []),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        jobs.append(new_job)
        
        return jsonify({
            'message': 'Job created successfully!',
            'job_id': new_job['id']
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Error creating job: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Smart Resume in simple mode (no database required)")
    print("Access the application at: http://localhost:5000")
    print("Or from other devices at: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
