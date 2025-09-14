#!/usr/bin/env python3
"""
Clean working Smart Resume app for testing login and PDF functionality
"""

from flask import Flask, render_template, jsonify, request, make_response
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'

# Enable CORS
CORS(app)

# Mock data
mock_users = {
    'test@example.com': {
        'id': '1',
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    }
}

mock_resumes = {
    '1': {
        'id': '1',
        'education': 'Bachelor of Computer Science - University of Technology (2018-2022)',
        'experience': 'Software Developer at Tech Corp (2022-2024)',
        'projects': 'Smart Resume Builder - Web application for creating resumes',
        'skills': 'Python, JavaScript, React, Flask, MongoDB',
        'created_at': '2024-01-15T10:30:00Z',
        'updated_at': '2024-01-15T15:45:00Z'
    }
}

# Mock jobs data
mock_jobs = {
    '1': {
        'id': '1',
        'job_title': 'Full Stack Developer',
        'company': 'Tech Innovations Inc.',
        'required_skills': ['Python', 'JavaScript', 'React', 'Flask', 'MongoDB'],
        'created_at': '2024-01-10T09:00:00Z',
        'updated_at': '2024-01-10T09:00:00Z'
    },
    '2': {
        'id': '2', 
        'job_title': 'Frontend Developer',
        'company': 'Digital Solutions Ltd.',
        'required_skills': ['JavaScript', 'React', 'HTML', 'CSS', 'Bootstrap'],
        'created_at': '2024-01-12T10:30:00Z',
        'updated_at': '2024-01-12T10:30:00Z'
    },
    '3': {
        'id': '3',
        'job_title': 'Backend Developer',
        'company': 'StartupXYZ',
        'required_skills': ['Python', 'Flask', 'PostgreSQL', 'Docker', 'AWS'],
        'created_at': '2024-01-14T14:15:00Z',
        'updated_at': '2024-01-14T14:15:00Z'
    },
    '4': {
        'id': '4',
        'job_title': 'Software Engineer',
        'company': 'Innovation Labs',
        'required_skills': ['Python', 'Django', 'React', 'PostgreSQL', 'Git'],
        'created_at': '2024-01-16T11:45:00Z',
        'updated_at': '2024-01-16T11:45:00Z'
    }
}

# Page Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/resumes')
def resumes_page():
    return render_template('resumes.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/jobs')
def jobs_page():
    return render_template('jobs.html')

# API Routes
@app.route('/api/status')
def api_status():
    return jsonify({
        "message": "API is running!",
        "status": "success",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        print("Login endpoint called")
        data = request.get_json()
        print(f"Login data: {data}")
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        user = mock_users.get(email)
        if user and user['password'] == password:
            return jsonify({
                'message': 'Login successful',
                'access_token': f'token-{user["id"]}',
                'refresh_token': f'refresh-{user["id"]}',
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'is_admin': False
                }
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/resumes', methods=['GET', 'POST'])
def resumes():
    if request.method == 'GET':
        try:
            print("Get resumes called")
            return jsonify({'resumes': list(mock_resumes.values())}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            print("Create resume called")
            data = request.get_json()
            
            new_id = str(len(mock_resumes) + 1)
            new_resume = {
                'id': new_id,
                'education': data.get('education', ''),
                'experience': data.get('experience', ''),
                'projects': data.get('projects', ''),
                'skills': data.get('skills', ''),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            mock_resumes[new_id] = new_resume
            print(f"Resume created with ID: {new_id}")
            
            return jsonify({
                'message': 'Resume created successfully',
                'resume_id': new_id
            }), 201
            
        except Exception as e:
            print(f"Create resume error: {e}")
            return jsonify({'message': str(e)}), 500

@app.route('/api/resumes/<resume_id>')
def get_resume(resume_id):
    try:
        print(f"Get resume {resume_id} called")
        resume = mock_resumes.get(resume_id)
        if resume:
            return jsonify({'resume': resume}), 200
        else:
            return jsonify({'message': 'Resume not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/resumes/<resume_id>/download')
def download_pdf(resume_id):
    try:
        print(f"Download PDF for resume {resume_id}")
        
        from xhtml2pdf import pisa
        from io import BytesIO
        
        resume = mock_resumes.get(resume_id)
        if not resume:
            return jsonify({'message': 'Resume not found'}), 404
        
        user = mock_users['test@example.com']
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ text-align: center; margin-bottom: 20px; }}
                .name {{ font-size: 24pt; font-weight: bold; }}
                .section {{ margin-bottom: 15px; }}
                .section-title {{ font-size: 14pt; font-weight: bold; text-transform: uppercase; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="name">{user['name']}</div>
                <div>{user['email']}</div>
            </div>
            
            <div class="section">
                <div class="section-title">Education</div>
                <div>{resume['education']}</div>
            </div>
            
            <div class="section">
                <div class="section-title">Experience</div>
                <div>{resume['experience']}</div>
            </div>
            
            <div class="section">
                <div class="section-title">Projects</div>
                <div>{resume['projects']}</div>
            </div>
            
            <div class="section">
                <div class="section-title">Skills</div>
                <div>{resume['skills']}</div>
            </div>
        </body>
        </html>
        """
        
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
        
        if pdf.err:
            return jsonify({'message': 'PDF generation failed'}), 500
        
        response = make_response(result.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{user["name"]}_Resume.pdf"'
        
        return response
        
    except Exception as e:
        print(f"Download error: {e}")
        return jsonify({'message': str(e)}), 500

# Jobs API endpoints
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        print("Get jobs called")
        return jsonify({'jobs': list(mock_jobs.values())}), 200
    except Exception as e:
        print(f"Get jobs error: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/jobs/<job_id>')
def get_job(job_id):
    try:
        print(f"Get job {job_id} called")
        job = mock_jobs.get(job_id)
        if job:
            return jsonify({'job': job}), 200
        else:
            return jsonify({'message': 'Job not found'}), 404
    except Exception as e:
        print(f"Get job error: {e}")
        return jsonify({'message': str(e)}), 500

@app.before_request
def log_requests():
    print(f"[{datetime.now()}] {request.method} {request.path}")

if __name__ == '__main__':
    print("\n🚀 Starting Smart Resume App...")
    print("📧 Login with: test@example.com / password123")
    print("🌐 URL: http://localhost:5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
