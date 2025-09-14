#!/usr/bin/env python3
"""
Simplified Smart Resume app that can run without database connection issues
"""

from flask import Flask, render_template, jsonify, request, make_response, redirect, url_for, session
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'simple-test-key-for-development'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Helper functions for authentication
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def find_user_by_email(email):
    """Find user by email (case-insensitive)"""
    if not email:
        return None
    
    email_lower = email.lower().strip()
    for user_email, user_data in mock_users.items():
        if user_email.lower() == email_lower:
            return user_data
    return None

def authenticate_user(email, password):
    """Authenticate user with email and password"""
    try:
        # Find user by email (case-insensitive)
        user = find_user_by_email(email)
        if not user:
            return None, "Invalid email or password"
        
        # Check if user is active
        if not user.get('is_active', True):
            return None, "Account is deactivated"
        
        # Verify password
        if check_password_hash(user['password_hash'], password):
            return user, None
        else:
            return None, "Invalid email or password"
            
    except Exception as e:
        print(f"Authentication error: {e}")
        return None, "Authentication system error"

# Mock data for testing login and PDF functionality
# Note: In production, use a proper database
mock_users = {
    'test@example.com': {
        'id': '1',
        'name': 'Test User',
        'email': 'test@example.com',
        'password_hash': generate_password_hash('password123'),
        'created_at': '2024-01-01T00:00:00Z',
        'is_active': True
    },
    'demo@smartresume.com': {
        'id': '2',
        'name': 'Demo User', 
        'email': 'demo@smartresume.com',
        'password_hash': generate_password_hash('demo123'),
        'created_at': '2024-01-01T00:00:00Z',
        'is_active': True
    },
    'sweetyvp1611@gmail.com': {
        'id': '3',
        'name': 'Sweety VP',
        'email': 'sweetyvp1611@gmail.com',
        'password_hash': generate_password_hash('sweety123'),
        'created_at': '2024-01-01T00:00:00Z',
        'is_active': True
    },
    'sweetykp23hcs@student.mes.ac.in': {
        'id': '4',
        'name': 'Sweety KP',
        'email': 'sweetykp23hcs@student.mes.ac.in',
        'password_hash': generate_password_hash('student123'),
        'created_at': '2024-01-01T00:00:00Z',
        'is_active': True
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

# Mock jobs data
mock_jobs = {
    '1': {
        'id': '1',
        'job_title': 'Senior Python Developer',
        'company': 'Tech Innovations Inc.',
        'required_skills': ['Python', 'Flask', 'MongoDB', 'React', 'AWS'],
        'created_at': '2024-01-10T09:00:00Z',
        'updated_at': '2024-01-10T09:00:00Z'
    },
    '2': {
        'id': '2',
        'job_title': 'Full Stack Developer',
        'company': 'Digital Solutions Ltd.',
        'required_skills': ['JavaScript', 'React', 'Node.js', 'PostgreSQL', 'Docker'],
        'created_at': '2024-01-12T10:15:00Z',
        'updated_at': '2024-01-12T10:15:00Z'
    },
    '3': {
        'id': '3',
        'job_title': 'Frontend Developer',
        'company': 'Creative Studio Co.',
        'required_skills': ['JavaScript', 'React', 'HTML', 'CSS', 'Bootstrap'],
        'created_at': '2024-01-14T14:30:00Z',
        'updated_at': '2024-01-14T14:30:00Z'
    },
    '4': {
        'id': '4',
        'job_title': 'DevOps Engineer',
        'company': 'Cloud Systems Pro',
        'required_skills': ['Python', 'Docker', 'Kubernetes', 'AWS', 'Git'],
        'created_at': '2024-01-16T11:20:00Z',
        'updated_at': '2024-01-16T11:20:00Z'
    },
    '5': {
        'id': '5',
        'job_title': 'Data Scientist',
        'company': 'Analytics Corp',
        'required_skills': ['Python', 'Machine Learning', 'MongoDB', 'PostgreSQL', 'AWS'],
        'created_at': '2024-01-18T13:45:00Z',
        'updated_at': '2024-01-18T13:45:00Z'
    }
}

# Page routes
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

# API routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Enhanced login route with proper authentication"""
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided. Please send email and password.'
            }), 400
            
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Basic input validation
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Validate email format
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Please enter a valid email address'
            }), 400
        
        print(f"🔐 Login attempt for: {email}")  # Debug log
        
        # Authenticate user
        user, error_message = authenticate_user(email, password)
        
        if user:
            # Create session
            session.permanent = True
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_name'] = user['name']
            session['login_time'] = datetime.utcnow().isoformat()
            
            # Generate tokens (in production, use proper JWT)
            import secrets
            access_token = f"token-{user['id']}-{secrets.token_hex(16)}"
            refresh_token = f"refresh-{user['id']}-{secrets.token_hex(16)}"
            
            print(f"✅ Login successful for: {email}")
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'is_admin': False
                },
                'redirect_url': '/dashboard'
            }), 200
        else:
            print(f"❌ Login failed for: {email} - {error_message}")
            return jsonify({
                'success': False,
                'message': error_message
            }), 401
            
    except ValueError as e:
        print(f"❌ Validation error during login: {e}")
        return jsonify({
            'success': False,
            'message': 'Invalid input data format'
        }), 400
        
    except Exception as e:
        print(f"❌ Unexpected error during login: {e}")
        return jsonify({
            'success': False,
            'message': 'Authentication service temporarily unavailable. Please try again later.'
        }), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout route to clear session"""
    try:
        user_email = session.get('user_email', 'unknown')
        
        # Clear session
        session.clear()
        
        print(f"🚪 User logged out: {user_email}")
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully',
            'redirect_url': '/login'
        }), 200
        
    except Exception as e:
        print(f"❌ Logout error: {e}")
        return jsonify({
            'success': False,
            'message': 'Error during logout'
        }), 500

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Check authentication status"""
    try:
        if 'user_id' in session:
            user_id = session.get('user_id')
            user_email = session.get('user_email')
            user_name = session.get('user_name')
            
            return jsonify({
                'authenticated': True,
                'user': {
                    'id': user_id,
                    'email': user_email,
                    'name': user_name
                }
            }), 200
        else:
            return jsonify({
                'authenticated': False
            }), 200
            
    except Exception as e:
        print(f"❌ Auth status error: {e}")
        return jsonify({
            'authenticated': False,
            'error': 'Unable to check authentication status'
        }), 500

@app.route('/api/resumes', methods=['GET', 'POST'])
def handle_resumes():
    if request.method == 'GET':
        try:
            return jsonify({
            'resumes': list(mock_resumes.values())
            }), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'message': 'No data provided'}), 400
            
            # Generate new resume ID
            new_id = str(len(mock_resumes) + 1)
            
            # Create new resume with current timestamp
            import datetime
            current_time = datetime.datetime.utcnow().isoformat() + 'Z'
            
            new_resume = {
                'id': new_id,
                'full_name': data.get('full_name', ''),
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'linkedin': data.get('linkedin', ''),
                'address': data.get('address', ''),
                'summary': data.get('summary', ''),
                'education': data.get('education', ''),
                'experience': data.get('experience', ''),
                'projects': data.get('projects', ''),
                'skills': data.get('skills', ''),
                'created_at': current_time,
                'updated_at': current_time
            }
            
            # Add to mock data
            mock_resumes[new_id] = new_resume
            
            print(f"✅ Created new resume with ID: {new_id}")  # Debug log
            
            return jsonify({
                'message': 'Resume created successfully',
                'resume': new_resume
            }), 201
            
        except Exception as e:
            print(f"❌ Error creating resume: {e}")  # Debug log
            return jsonify({'message': f'Error creating resume: {str(e)}'}), 500

@app.route('/api/resumes/<resume_id>', methods=['GET', 'PUT', 'DELETE'])
def mock_resume_operations(resume_id):
    if request.method == 'GET':
        try:
            resume = mock_resumes.get(resume_id)
            if resume:
                return jsonify({'resume': resume}), 200
            else:
                return jsonify({'message': 'Resume not found'}), 404
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'message': 'No data provided'}), 400
            
            resume = mock_resumes.get(resume_id)
            if not resume:
                return jsonify({'message': 'Resume not found'}), 404
            
            # Update resume with current timestamp
            import datetime
            current_time = datetime.datetime.utcnow().isoformat() + 'Z'
            
            # Update fields
            resume.update({
                'full_name': data.get('full_name', resume.get('full_name', '')),
                'email': data.get('email', resume.get('email', '')),
                'phone': data.get('phone', resume.get('phone', '')),
                'linkedin': data.get('linkedin', resume.get('linkedin', '')),
                'address': data.get('address', resume.get('address', '')),
                'summary': data.get('summary', resume.get('summary', '')),
                'education': data.get('education', resume.get('education', '')),
                'experience': data.get('experience', resume.get('experience', '')),
                'projects': data.get('projects', resume.get('projects', '')),
                'skills': data.get('skills', resume.get('skills', '')),
                'updated_at': current_time
            })
            
            print(f"✅ Updated resume with ID: {resume_id}")  # Debug log
            
            return jsonify({
                'message': 'Resume updated successfully',
                'resume': resume
            }), 200
            
        except Exception as e:
            print(f"❌ Error updating resume: {e}")  # Debug log
            return jsonify({'message': f'Error updating resume: {str(e)}'}), 500
    
    elif request.method == 'DELETE':
        try:
            if resume_id not in mock_resumes:
                return jsonify({'message': 'Resume not found'}), 404
            
            # Delete the resume
            deleted_resume = mock_resumes.pop(resume_id)
            
            print(f"✅ Deleted resume with ID: {resume_id}")  # Debug log
            
            return jsonify({
                'message': 'Resume deleted successfully',
                'resume': deleted_resume
            }), 200
            
        except Exception as e:
            print(f"❌ Error deleting resume: {e}")  # Debug log
            return jsonify({'message': f'Error deleting resume: {str(e)}'}), 500

@app.route('/api/jobs', methods=['GET'])
def mock_get_jobs():
    try:
        return jsonify({
            'jobs': list(mock_jobs.values())
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/jobs/<job_id>')
def mock_get_job(job_id):
    try:
        job = mock_jobs.get(job_id)
        if job:
            return jsonify({'job': job}), 200
        else:
            return jsonify({'message': 'Job not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/resumes/<resume_id>/download')
def mock_download_resume(resume_id):
    """Test the PDF download functionality"""
    try:
        print(f"PDF download requested for resume: {resume_id}")  # Debug log
        
        from xhtml2pdf import pisa
        from io import BytesIO
        
        resume = mock_resumes.get(resume_id)
        if not resume:
            return jsonify({'message': 'Resume not found'}), 404
        
        # Validate resume has required data for PDF generation
        if not resume.get('full_name') and not resume.get('email'):
            return jsonify({'message': 'Resume data incomplete - missing name or email'}), 400
        
        # Generate contact info section
        contact_info_parts = []
        if resume.get('email'):
            contact_info_parts.append(resume['email'])
        if resume.get('phone'):
            contact_info_parts.append(resume['phone'])
        if resume.get('address'):
            contact_info_parts.append(resume['address'])
        if resume.get('linkedin'):
            contact_info_parts.append(resume['linkedin'])
        
        contact_info = ' | '.join(contact_info_parts) if contact_info_parts else ''
        
        # Generate sections dynamically based on available data
        sections_html = ''
        
        # Professional Summary
        if resume.get('summary'):
            sections_html += f"""
            <div class="section">
                <div class="section-title">Professional Summary</div>
                <div class="section-content">{resume['summary']}</div>
            </div>
            """
        
        # Education
        if resume.get('education'):
            sections_html += f"""
            <div class="section">
                <div class="section-title">Education</div>
                <div class="section-content">{resume['education']}</div>
            </div>
            """
        
        # Experience
        if resume.get('experience'):
            sections_html += f"""
            <div class="section">
                <div class="section-title">Work Experience</div>
                <div class="section-content">{resume['experience']}</div>
            </div>
            """
        
        # Projects
        if resume.get('projects'):
            sections_html += f"""
            <div class="section">
                <div class="section-title">Projects</div>
                <div class="section-content">{resume['projects']}</div>
            </div>
            """
        
        # Skills
        skills_html = ''
        if resume.get('skills'):
            skills = [skill.strip() for skill in resume['skills'].split(',') if skill.strip()]
            if skills:
                skills_html = ' '.join([f'<span class="skill-item">{skill}</span>' for skill in skills])
                sections_html += f"""
                <div class="section">
                    <div class="section-title">Skills</div>
                    <div class="skills-list">
                        {skills_html}
                    </div>
                </div>
                """
        
        # If no content sections, show a message
        if not sections_html.strip():
            sections_html = '<div class="section"><div class="section-content">No additional information available.</div></div>'
        
        # Generate PDF HTML template with actual resume data
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
                    margin-bottom: 10px;
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
                <div class="name">{resume.get('full_name', 'No Name Provided')}</div>
                <div class="contact-info">{contact_info}</div>
            </div>
            
            {sections_html}
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
        
        # Create response with dynamic filename
        safe_filename = resume.get('full_name', 'Resume').replace(' ', '_').replace('/', '_')
        response = make_response(result.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{safe_filename}_Resume.pdf"'
        
        return response
        
    except Exception as e:
        print(f"Download error: {e}")  # Debug log
        return jsonify({'message': f'Download error: {str(e)}'}), 500

@app.route('/api/resumes/<resume_id>/print')
def print_resume(resume_id):
    """Generate HTML view for printing resume"""
    try:
        print(f"Print view requested for resume: {resume_id}")  # Debug log
        
        resume = mock_resumes.get(resume_id)
        if not resume:
            return f"<html><body><h1>Resume not found</h1><p>Resume with ID '{resume_id}' was not found.</p></body></html>", 404
        
        # Validate resume has required data
        if not resume.get('full_name') and not resume.get('email'):
            return f"<html><body><h1>Incomplete Resume</h1><p>Resume data is missing required information.</p></body></html>", 400
        
        # Generate contact info section
        contact_info_parts = []
        if resume.get('email'):
            contact_info_parts.append(resume['email'])
        if resume.get('phone'):
            contact_info_parts.append(resume['phone'])
        if resume.get('address'):
            contact_info_parts.append(resume['address'])
        if resume.get('linkedin'):
            contact_info_parts.append(resume['linkedin'])
        
        contact_info = ' | '.join(contact_info_parts) if contact_info_parts else ''
        
        # Generate sections dynamically
        sections_html = ''
        
        # Professional Summary
        if resume.get('summary'):
            sections_html += f"""
            <div class="section">
                <div class="section-title">Professional Summary</div>
                <div class="section-content">{resume['summary']}</div>
            </div>
            """
        
        # Education
        if resume.get('education'):
            sections_html += f"""
            <div class="section">
                <div class="section-title">Education</div>
                <div class="section-content">{resume['education']}</div>
            </div>
            """
        
        # Experience
        if resume.get('experience'):
            sections_html += f"""
            <div class="section">
                <div class="section-title">Work Experience</div>
                <div class="section-content">{resume['experience']}</div>
            </div>
            """
        
        # Projects
        if resume.get('projects'):
            sections_html += f"""
            <div class="section">
                <div class="section-title">Projects</div>
                <div class="section-content">{resume['projects']}</div>
            </div>
            """
        
        # Skills
        if resume.get('skills'):
            skills = [skill.strip() for skill in resume['skills'].split(',') if skill.strip()]
            if skills:
                skills_html = ' '.join([f'<span class="skill-item">{skill}</span>' for skill in skills])
                sections_html += f"""
                <div class="section">
                    <div class="section-title">Skills</div>
                    <div class="skills-list">
                        {skills_html}
                    </div>
                </div>
                """
        
        # If no content sections, show a message
        if not sections_html.strip():
            sections_html = '<div class="section"><div class="section-content">No additional information available.</div></div>'
        
        # Generate HTML for printing with enhanced print styles
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{resume.get('full_name', 'Resume')} - Resume</title>
            <style>
                @media print {{
                    @page {{
                        margin: 0.75in;
                    }}
                    body {{
                        -webkit-print-color-adjust: exact;
                    }}
                }}
                body {{
                    font-family: 'Arial', sans-serif;
                    font-size: 12pt;
                    line-height: 1.4;
                    color: #333;
                    margin: 20px;
                    max-width: 8.5in;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 2px solid #2c3e50;
                    padding-bottom: 15px;
                    margin-bottom: 25px;
                }}
                .name {{
                    font-size: 28pt;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 8px;
                }}
                .contact-info {{
                    font-size: 11pt;
                    color: #7f8c8d;
                    margin-bottom: 10px;
                }}
                .section {{
                    margin-bottom: 25px;
                    page-break-inside: avoid;
                }}
                .section-title {{
                    font-size: 16pt;
                    font-weight: bold;
                    color: #2c3e50;
                    border-bottom: 1px solid #bdc3c7;
                    padding-bottom: 5px;
                    margin-bottom: 12px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .section-content {{
                    margin-left: 10px;
                    text-align: justify;
                    white-space: pre-wrap;
                    line-height: 1.5;
                }}
                .skills-list {{
                    margin-left: 10px;
                    line-height: 1.8;
                }}
                .skill-item {{
                    background-color: #ecf0f1;
                    padding: 6px 14px;
                    margin: 3px;
                    border-radius: 15px;
                    font-size: 10pt;
                    color: #2c3e50;
                    border: 1px solid #bdc3c7;
                    display: inline-block;
                }}
            </style>
            <script>
                // Auto-trigger print dialog when page loads
                window.onload = function() {{
                    window.print();
                }};
            </script>
        </head>
        <body>
            <div class="header">
                <div class="name">{resume.get('full_name', 'No Name Provided')}</div>
                <div class="contact-info">{contact_info}</div>
            </div>
            
            {sections_html}
        </body>
        </html>
        """
        
        print(f"Print HTML generated successfully for resume: {resume_id}")
        return html_template, 200, {'Content-Type': 'text/html'}
        
    except Exception as e:
        print(f"Print error: {e}")  # Debug log
        error_html = f"<html><body><h1>Print Error</h1><p>Error generating print view: {str(e)}</p></body></html>"
        return error_html, 500, {'Content-Type': 'text/html'}

@app.route('/test-db')
def test_db():
    return jsonify({
        "database_status": "working",
        "tables": {
            "users": f"{len(mock_users)} documents",
            "resumes": f"{len(mock_resumes)} documents",
            "jobs": f"{len(mock_jobs)} documents"
        },
        "message": "Mock database is working fine!"
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        "message": "Smart Resume Simple API is running!",
        "status": "success",
        "mode": "simplified",
        "endpoints": {
            "login": "/api/auth/login",
            "resumes": "/api/resumes",
            "jobs": "/api/jobs",
            "download": "/api/resumes/<id>/download",
            "test_db": "/test-db"
        }
    })

@app.route('/favicon.ico')
def favicon():
    """Return a simple response for favicon to prevent 404 errors"""
    return '', 204  # No content response

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Smart Resume Simple Application...")
    print("=" * 60)
    print("📝 Test Login Credentials (Email & Password):")
    print("   • test@example.com / password123")
    print("   • demo@smartresume.com / demo123")
    print("   • sweetyvp1611@gmail.com / sweety123")
    print("   • sweetykp23hcs@student.mes.ac.in / student123")
    print("")
    print("🔐 Security Features:")
    print("   • Password hashing with bcrypt")
    print("   • Case-insensitive email lookup")
    print("   • Session management")
    print("   • Enhanced error handling")
    print("=" * 60)
    print("🌐 Access URLs:")
    print("   Local: http://localhost:5000")
    print("   Login: http://localhost:5000/login")
    print("   API Status: http://localhost:5000/api/status")
    print("=" * 60)
    print("✨ Features available:")
    print("   • Login page (working)")
    print("   • Resume listing")
    print("   • PDF download")
    print("   • Print functionality")
    print("=" * 60)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("Make sure port 5000 is not already in use.")
