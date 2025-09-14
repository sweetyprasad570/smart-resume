#!/usr/bin/env python3
"""
Working Smart Resume app with proper endpoint registration and PDF functionality
"""

from flask import Flask, render_template, jsonify, request, make_response
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'working-app-secret-key'

# Enable CORS for API calls
CORS(app)

# Mock data for testing login and PDF functionality
mock_users = {
    'test@example.com': {
        'id': '1',
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    },
    'demo@smartresume.com': {
        'id': '2', 
        'name': 'Demo User',
        'email': 'demo@smartresume.com',
        'password': 'demo123'
    }
}

mock_resumes = {
    '1': {
        'id': '1',
        'education': 'Bachelor of Computer Science - University of Technology (2018-2022)\nGPA: 3.8/4.0\nRelevant Coursework: Data Structures, Algorithms, Web Development, Database Systems',
        'experience': 'Software Developer at Tech Corp (2022-2024)\n• Developed and maintained web applications using Python and Flask\n• Collaborated with cross-functional teams to deliver high-quality software solutions\n• Improved application performance by 30% through code optimization\n\nJunior Developer at StartupXYZ (2021-2022)\n• Built responsive web interfaces using HTML, CSS, and JavaScript\n• Participated in agile development processes and code reviews\n• Assisted in database design and optimization',
        'projects': 'Smart Resume Builder (2024)\n• Web application for creating professional resumes with PDF export functionality\n• Built with Flask, MongoDB, Bootstrap, and xhtml2pdf\n• Features: User authentication, resume templates, real-time editing\n\nE-commerce Platform (2023)\n• Full-stack web application with payment integration\n• Technologies: Python, Flask, PostgreSQL, Stripe API\n• Implemented shopping cart, user accounts, and order management\n\nTask Management API (2023)\n• RESTful API for task and project management\n• Built with Flask, SQLAlchemy, JWT authentication\n• Features: CRUD operations, user roles, task assignment',
        'skills': 'Python, JavaScript, React, Flask, MongoDB, PostgreSQL, HTML, CSS, Bootstrap, Git, Docker, AWS',
        'created_at': '2024-01-15T10:30:00Z',
        'updated_at': '2024-01-15T15:45:00Z'
    },
    '2': {
        'id': '2',
        'education': 'Master of Software Engineering - Tech Institute (2020-2022)\nBachelor of Information Technology - State University (2016-2020)',
        'experience': 'Senior Full-Stack Developer at Innovation Labs (2023-Present)\n• Lead development team of 5 developers\n• Architect scalable web applications\n• Mentor junior developers\n\nFull-Stack Developer at Digital Solutions (2022-2023)\n• Developed client-facing web applications\n• Integrated third-party APIs and services',
        'projects': 'Cloud-based CRM System\nAI-powered Analytics Dashboard\nMobile-first E-learning Platform',
        'skills': 'Python, JavaScript, React, Node.js, Flask, Django, MongoDB, PostgreSQL, AWS, Docker, Kubernetes',
        'created_at': '2024-02-01T09:15:00Z',
        'updated_at': '2024-02-01T09:15:00Z'
    }
}

# ==================== PAGE ROUTES ====================

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/login')
def login_page():
    """Login page"""
    return render_template('login.html')

@app.route('/register')
def register_page():
    """Registration page"""
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@app.route('/resumes')
def resumes_page():
    """Resumes page"""
    return render_template('resumes.html')

@app.route('/jobs')
def jobs_page():
    """Jobs page"""
    return render_template('jobs.html')

# ==================== API ROUTES ====================

@app.route('/api/status', methods=['GET'])
def api_status():
    """API status endpoint"""
    return jsonify({
        "message": "Smart Resume API is running!",
        "status": "success",
        "mode": "working_version",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "login": "POST /api/auth/login",
            "resumes": "GET /api/resumes", 
            "resume_detail": "GET /api/resumes/<id>",
            "download_pdf": "GET /api/resumes/<id>/download"
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "database": "mock_data",
        "timestamp": datetime.now().isoformat()
    })

# ==================== AUTH ROUTES ====================

@app.route('/api/auth/login', methods=['POST'])
def login_api():
    """Login API endpoint"""
    try:
        print("Login endpoint called")  # Debug log
        
        data = request.get_json()
        if not data:
            print("No JSON data received")  # Debug log
            return jsonify({'message': 'No data provided'}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        print(f"Login attempt for email: {email}")  # Debug log
        
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400
        
        user = mock_users.get(email)
        if user and user['password'] == password:
            print(f"Login successful for: {email}")  # Debug log
            return jsonify({
                'message': 'Login successful',
                'access_token': f'mock-token-{user["id"]}-{datetime.now().timestamp()}',
                'refresh_token': f'mock-refresh-{user["id"]}-{datetime.now().timestamp()}',
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'is_admin': False
                }
            }), 200
        else:
            print(f"Invalid credentials for: {email}")  # Debug log
            return jsonify({'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")  # Debug log
        return jsonify({'message': f'Server error: {str(e)}'}), 500

@app.route('/api/auth/register', methods=['POST'])
def register_api():
    """Registration API endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
            
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not all([name, email, password]):
            return jsonify({'message': 'Name, email, and password are required'}), 400
        
        if email in mock_users:
            return jsonify({'message': 'Email already registered'}), 400
        
        # Add new user to mock data
        new_id = str(len(mock_users) + 1)
        mock_users[email] = {
            'id': new_id,
            'name': name,
            'email': email,
            'password': password
        }
        
        return jsonify({
            'message': 'Registration successful',
            'user_id': new_id
        }), 201
            
    except Exception as e:
        print(f"Registration error: {e}")  # Debug log
        return jsonify({'message': f'Server error: {str(e)}'}), 500

# ==================== RESUME ROUTES ====================

@app.route('/api/resumes', methods=['GET', 'POST'])
def handle_resumes():
    """Handle both GET (list resumes) and POST (create resume)"""
    if request.method == 'GET':
        try:
            print("Get resumes endpoint called")  # Debug log
            return jsonify({
                'resumes': list(mock_resumes.values())
            }), 200
        except Exception as e:
            print(f"Get resumes error: {e}")  # Debug log
            return jsonify({'message': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            print("Create resume endpoint called")  # Debug log
            
            data = request.get_json()
            if not data:
                return jsonify({'message': 'No data provided'}), 400
            
            # Generate new resume ID
            new_id = str(len(mock_resumes) + 1)
            
            # Create new resume
            new_resume = {
                'id': new_id,
                'education': data.get('education', ''),
                'experience': data.get('experience', ''),
                'projects': data.get('projects', ''),
                'skills': data.get('skills', ''),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Add to mock data
            mock_resumes[new_id] = new_resume
            
            print(f"Resume created with ID: {new_id}")  # Debug log
            
            return jsonify({
                'message': 'Resume created successfully',
                'resume_id': new_id
            }), 201
            
        except Exception as e:
            print(f"Create resume error: {e}")  # Debug log
            return jsonify({'message': f'Server error: {str(e)}'}), 500

@app.route('/api/resumes/<resume_id>', methods=['GET'])
def get_resume(resume_id):
    """Get specific resume"""
    try:
        print(f"Get resume endpoint called for ID: {resume_id}")  # Debug log
        resume = mock_resumes.get(resume_id)
        if resume:
            return jsonify({'resume': resume}), 200
        else:
            return jsonify({'message': 'Resume not found'}), 404
    except Exception as e:
        print(f"Get resume error: {e}")  # Debug log
        return jsonify({'message': str(e)}), 500

@app.route('/api/resumes/<resume_id>', methods=['PUT'])
def update_resume(resume_id):
    """Update existing resume"""
    try:
        print(f"Update resume endpoint called for ID: {resume_id}")  # Debug log
        
        resume = mock_resumes.get(resume_id)
        if not resume:
            return jsonify({'message': 'Resume not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        # Update resume fields
        if 'education' in data:
            resume['education'] = data['education']
        if 'experience' in data:
            resume['experience'] = data['experience']
        if 'projects' in data:
            resume['projects'] = data['projects']
        if 'skills' in data:
            resume['skills'] = data['skills']
        
        resume['updated_at'] = datetime.now().isoformat()
        
        print(f"Resume {resume_id} updated successfully")  # Debug log
        
        return jsonify({'message': 'Resume updated successfully'}), 200
        
    except Exception as e:
        print(f"Update resume error: {e}")  # Debug log
        return jsonify({'message': str(e)}), 500

@app.route('/api/resumes/<resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    """Delete resume"""
    try:
        print(f"Delete resume endpoint called for ID: {resume_id}")  # Debug log
        
        if resume_id not in mock_resumes:
            return jsonify({'message': 'Resume not found'}), 404
        
        del mock_resumes[resume_id]
        
        print(f"Resume {resume_id} deleted successfully")  # Debug log
        
        return jsonify({'message': 'Resume deleted successfully'}), 200
        
    except Exception as e:
        print(f"Delete resume error: {e}")  # Debug log
        return jsonify({'message': str(e)}), 500

@app.route('/api/resumes/<resume_id>/download', methods=['GET'])
def download_resume_pdf(resume_id):
    """Download resume as PDF"""
    try:
        print(f"PDF download requested for resume: {resume_id}")  # Debug log
        
        # Import PDF generation library
        try:
            from xhtml2pdf import pisa
            from io import BytesIO
        except ImportError as e:
            return jsonify({'message': f'PDF library not available: {str(e)}'}), 500
        
        resume = mock_resumes.get(resume_id)
        if not resume:
            return jsonify({'message': 'Resume not found'}), 404
        
        # Get user for this resume (simplified mapping)
        user = mock_users['test@example.com'] if resume_id == '1' else mock_users['demo@smartresume.com']
        
        # Generate PDF HTML template
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @page {{
                    size: A4;
                    margin: 1in;
                }}
                body {{
                    font-family: 'Arial', sans-serif;
                    font-size: 11pt;
                    line-height: 1.4;
                    color: #333;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 2px solid #2c3e50;
                    padding-bottom: 15px;
                    margin-bottom: 25px;
                }}
                .name {{
                    font-size: 24pt;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 5px;
                }}
                .contact-info {{
                    font-size: 10pt;
                    color: #7f8c8d;
                }}
                .section {{
                    margin-bottom: 20px;
                }}
                .section-title {{
                    font-size: 14pt;
                    font-weight: bold;
                    color: #2c3e50;
                    border-bottom: 1px solid #bdc3c7;
                    padding-bottom: 5px;
                    margin-bottom: 10px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .section-content {{
                    margin-left: 10px;
                    text-align: justify;
                    white-space: pre-wrap;
                }}
                .skills-list {{
                    margin-left: 10px;
                }}
                .skill-item {{
                    background-color: #ecf0f1;
                    padding: 4px 12px;
                    margin: 2px;
                    border-radius: 15px;
                    font-size: 9pt;
                    color: #2c3e50;
                    border: 1px solid #bdc3c7;
                    display: inline-block;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="name">{user['name']}</div>
                <div class="contact-info">{user['email']}</div>
            </div>
            
            <div class="section">
                <div class="section-title">Education</div>
                <div class="section-content">{resume.get('education', 'No education information provided')}</div>
            </div>
            
            <div class="section">
                <div class="section-title">Experience</div>
                <div class="section-content">{resume.get('experience', 'No experience information provided')}</div>
            </div>
            
            <div class="section">
                <div class="section-title">Projects</div>
                <div class="section-content">{resume.get('projects', 'No projects listed')}</div>
            </div>
            
            <div class="section">
                <div class="section-title">Skills</div>
                <div class="skills-list">
                    {' '.join([f'<span class="skill-item">{skill.strip()}</span>' for skill in resume.get('skills', '').split(',') if skill.strip()])}
                </div>
            </div>
        </body>
        </html>
        """
        
        # Generate PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_template.encode("utf-8")), result)
        
        if pdf.err:
            print(f"PDF generation errors: {pdf.err}")  # Debug log
            return jsonify({'message': 'Error generating PDF'}), 500
        
        print(f"PDF generated successfully, size: {len(result.getvalue())} bytes")  # Debug log
        
        # Create response
        response = make_response(result.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{user["name"].replace(" ", "_")}_Resume.pdf"'
        
        return response
        
    except Exception as e:
        print(f"Download error: {e}")  # Debug log
        return jsonify({'message': f'Download error: {str(e)}'}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    print(f"404 Error: {request.url}")  # Debug log
    if request.path.startswith('/api/'):
        return jsonify({'message': f'API endpoint not found: {request.path}'}), 404
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    print(f"500 Error: {error}")  # Debug log
    return jsonify({'message': 'Internal server error'}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    print(f"405 Error: {request.method} {request.path}")  # Debug log
    return jsonify({'message': f'Method {request.method} not allowed for {request.path}'}), 405

# ==================== DEBUG ROUTES ====================

@app.route('/debug/routes')
def debug_routes():
    """Debug endpoint to show all available routes"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'path': rule.rule
        })
    return jsonify({'routes': routes})

@app.route('/debug/test-pdf')
def test_pdf_generation():
    """Test PDF generation independently"""
    try:
        from xhtml2pdf import pisa
        from io import BytesIO
        
        html = """
        <html><body>
        <h1>PDF Test</h1>
        <p>This is a test PDF generation.</p>
        </body></html>
        """
        
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
        
        if pdf.err:
            return jsonify({'status': 'error', 'message': 'PDF generation failed'}), 500
        
        response = make_response(result.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename="test.pdf"'
        
        return response
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ==================== REQUEST LOGGING ====================

@app.before_request
def log_request_info():
    """Log all incoming requests for debugging"""
    print(f"[{datetime.now()}] {request.method} {request.path} from {request.remote_addr}")
    if request.is_json:
        print(f"Request data: {request.get_json()}")

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 Starting Smart Resume Working Application...")
    print("=" * 80)
    print("📝 Test Login Credentials:")
    print("   Email: test@example.com")
    print("   Password: password123")
    print("")
    print("   Email: demo@smartresume.com") 
    print("   Password: demo123")
    print("=" * 80)
    print("🌐 Access URLs:")
    print("   Home: http://localhost:5000")
    print("   Login: http://localhost:5000/login")
    print("   Resumes: http://localhost:5000/resumes")
    print("   API Status: http://localhost:5000/api/status")
    print("   Debug Routes: http://localhost:5000/debug/routes")
    print("   Test PDF: http://localhost:5000/debug/test-pdf")
    print("=" * 80)
    print("✨ Available API Endpoints:")
    print("   POST /api/auth/login")
    print("   POST /api/auth/register")
    print("   GET  /api/resumes")
    print("   GET  /api/resumes/<id>")
    print("   GET  /api/resumes/<id>/download")
    print("   GET  /api/status")
    print("=" * 80)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("Make sure port 5000 is not already in use.")
        print("Try running: netstat -ano | findstr :5000")
