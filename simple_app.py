from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import bcrypt
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Required for sessions
CORS(app)

# Add current_user context processor for templates
@app.context_processor
def inject_current_user():
    current_user = 'user_id' in session
    user_data = None
    
    if current_user:
        user_data = {
            'id': session.get('user_id'),
            'name': session.get('user_name', 'User'),
            'email': session.get('user_email', '')
        }
    
    return dict(
        current_user=current_user,
        user_data=user_data
    )

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

@app.route('/view-profile')
def view_profile():
    if not is_logged_in():
        return redirect(url_for('login_page'))
    return render_template('view_profile.html')

@app.route('/edit-profile')
def edit_profile():
    if not is_logged_in():
        return redirect(url_for('login_page'))
    return render_template('edit_profile.html')

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

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        print(f"=== LOGIN ATTEMPT ===")
        print(f"Email: {email}")
        print(f"Total users in system: {len(users)}")
        
        # Validate input
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400
        
        # Find user by email
        user = None
        for u in users:
            if u['email'].lower() == email:
                user = u
                break
        
        if not user:
            print(f"User not found with email: {email}")
            print("Creating demo user for direct login...")
            # Create a demo user automatically for direct login
            demo_user = {
                'id': str(uuid.uuid4()),
                'name': email.split('@')[0].title(),  # Use email prefix as name
                'email': email,
                'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                'created_at': datetime.now().isoformat()
            }
            users.append(demo_user)
            user = demo_user
            print(f"Demo user created: {user['name']} ({user['email']})")
        
        # Verify password
        try:
            password_bytes = password.encode('utf-8')
            hashed_password = user['password'].encode('utf-8')
            
            if bcrypt.checkpw(password_bytes, hashed_password):
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
                print("Password verification failed")
                return jsonify({'message': 'Invalid email or password'}), 401
                
        except Exception as password_error:
            print(f"Password verification error: {password_error}")
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
        
        # Validate input
        if not name or not email or not password:
            return jsonify({'message': 'Name, email and password are required'}), 400
        
        if len(password) < 6:
            return jsonify({'message': 'Password must be at least 6 characters long'}), 400
        
        # Check if user already exists
        for user in users:
            if user['email'].lower() == email:
                print(f"User already exists with email: {email}")
                return jsonify({'message': 'User with this email already exists'}), 409
        
        # Hash password
        try:
            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt)
            
            # Create new user
            new_user = {
                'id': str(uuid.uuid4()),
                'name': name,
                'email': email,
                'password': hashed_password.decode('utf-8'),  # Store as string
                'created_at': datetime.utcnow().isoformat()
            }
            
            users.append(new_user)
            
            print(f"User registered successfully: {name} ({email})")
            print(f"Total users now: {len(users)}")
            print("=========================")
            
            return jsonify({
                'message': 'Registration successful! You can now login.',
                'status': 'success'
            }), 201
            
        except Exception as hash_error:
            print(f"Password hashing error: {hash_error}")
            return jsonify({'message': 'Registration failed. Please try again.'}), 500
            
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({'message': 'Registration failed. Please try again.'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    try:
        if 'user_id' in session:
            user_name = session.get('user_name', 'Unknown')
            session.clear()
            print(f"User logged out: {user_name}")
            return jsonify({'message': 'Logged out successfully'}), 200
        else:
            return jsonify({'message': 'Not logged in'}), 400
    except Exception as e:
        print(f"Logout error: {str(e)}")
        return jsonify({'message': 'Logout failed'}), 500

# User profile endpoint
@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    """Get current user profile data"""
    try:
        # Check if user is logged in
        if not is_logged_in():
            # Return a response that indicates user is not authenticated
            return jsonify({
                'authenticated': False,
                'message': 'User not logged in',
                'user': None
            }), 200
        
        current_user_id = session.get('user_id')
        user = next((u for u in users if u['id'] == current_user_id), None)
        
        if not user:
            return jsonify({
                'authenticated': False,
                'message': 'User not found',
                'user': None
            }), 404
        
        # Count user's resumes
        user_resumes = [resume for resume in resumes if resume['user_id'] == current_user_id]
        resume_count = len(user_resumes)
        
        # Return comprehensive user profile data
        return jsonify({
            'authenticated': True,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'is_admin': user.get('is_admin', False),
                'created_at': user.get('created_at', datetime.utcnow().isoformat()),
                'resume_count': resume_count,
                'personal_info': user.get('personal_info', {}),
                'professional_info': user.get('professional_info', {}),
                'education': user.get('education', []),
                'experience': user.get('experience', []),
                'skills': user.get('skills', []),
                'projects': user.get('projects', [])
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'authenticated': False,
            'message': f'Error: {str(e)}',
            'user': None
        }), 500

# User resume endpoint
@app.route('/api/user/resume', methods=['GET'])
def get_user_resume():
    """Get current user's resume data"""
    try:
        # Check if user is logged in
        if not is_logged_in():
            return jsonify({
                'authenticated': False,
                'message': 'User not logged in',
                'resume': None
            }), 200
        
        current_user_id = session.get('user_id')
        user = next((u for u in users if u['id'] == current_user_id), None)
        
        if not user:
            return jsonify({
                'authenticated': False,
                'message': 'User not found',
                'resume': None
            }), 404
        
        # Find user's resume
        user_resume = next((r for r in resumes if r['user_id'] == current_user_id), None)
        
        # If no resume exists, create sample data for the user
        if not user_resume:
            user_resume = {
                'id': str(uuid.uuid4()),
                'user_id': current_user_id,
                'full_name': user.get('name', 'John Doe'),
                'email': user.get('email', 'john@example.com'),
                'phone': '+1 (555) 123-4567',
                'linkedin': 'https://linkedin.com/in/johndoe',
                'address': 'San Francisco, CA',
                'summary': 'Experienced software developer with a passion for creating innovative solutions and leading teams to deliver high-quality products.',
                'education': 'Bachelor of Science in Computer Science\nUniversity of Technology\n2018 - 2022\nGPA: 3.8/4.0',
                'experience': 'Senior Software Developer\nTech Solutions Inc. | 2022 - Present\n- Led development of microservices architecture serving 1M+ users\n- Mentored junior developers and conducted code reviews\n- Implemented CI/CD pipelines reducing deployment time by 60%\n\nSoftware Developer\nStartupXYZ | 2020 - 2022\n- Developed full-stack web applications using React and Node.js\n- Collaborated with cross-functional teams to deliver features on time\n- Optimized database queries improving performance by 40%',
                'projects': 'E-commerce Platform\n| React, Node.js, MongoDB\n- Built scalable e-commerce platform with real-time inventory management\n- Implemented secure payment processing and user authentication\n- Achieved 99.9% uptime and handled 10K+ concurrent users\n\nTask Management System\n| Vue.js, Python, PostgreSQL\n- Developed comprehensive task management solution for teams\n- Integrated real-time notifications and collaboration features\n- Reduced project completion time by 25% for client teams',
                'skills': 'JavaScript, Python, React, Node.js, MongoDB, PostgreSQL, Docker, Kubernetes, AWS, Git, CI/CD, Agile, Scrum, TypeScript, Express.js, Flask, REST APIs, GraphQL, Microservices',
                'skill_ratings': {
                    'JavaScript': 9,
                    'Python': 8,
                    'React': 9,
                    'Node.js': 8,
                    'MongoDB': 7,
                    'PostgreSQL': 8,
                    'Docker': 7,
                    'Kubernetes': 6,
                    'AWS': 7,
                    'Git': 9,
                    'CI/CD': 8,
                    'Agile': 8,
                    'Scrum': 7
                },
                'profile_picture': '',
                'template_type': 'modern',
                'is_public': False,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            # Add the sample resume to the resumes list
            resumes.append(user_resume)
        
        # Return the resume data
        return jsonify({
            'authenticated': True,
            'resume': user_resume
        }), 200
        
    except Exception as e:
        return jsonify({
            'authenticated': False,
            'message': f'Error: {str(e)}',
            'resume': None
        }), 500

# Flask logout route for navbar form
@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    try:
        if 'user_id' in session:
            user_name = session.get('user_name', 'Unknown')
            session.clear()
            print(f"User logged out via form: {user_name}")
        return redirect('/')
    except Exception as e:
        print(f"Logout page error: {str(e)}")
        return redirect('/')

# Resume endpoints
@app.route('/api/resumes', methods=['POST'])
def create_resume():
    try:
        # Check if user is logged in
        if not is_logged_in():
            return jsonify({'message': 'Please login to create a resume'}), 401
        
        current_user_id = get_current_user_id()
        data = request.get_json()
        
        # Debug: Print received data
        print("=== CREATE RESUME DEBUG ===")
        print(f"Received data: {data}")
        print(f"Current user ID: {current_user_id}")
        
        new_resume = {
            'id': str(uuid.uuid4()),
            'user_id': current_user_id,
            # Personal Information
            'full_name': data.get('full_name', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'linkedin': data.get('linkedin', ''),
            'address': data.get('address', ''),
            'summary': data.get('summary', ''),
            # Resume Sections
            'education': data.get('education', ''),
            'experience': data.get('experience', ''),
            'projects': data.get('projects', ''),
            'skills': data.get('skills', ''),
            'skill_ratings': data.get('skill_ratings', {}),
            # Additional Fields
            'profile_picture': data.get('profile_picture', ''),
            'template_type': data.get('template_type', 'modern'),
            'is_public': data.get('is_public', False),
            # Timestamps
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        print(f"New resume object: {new_resume}")
        print("===========================")
        
        resumes.append(new_resume)
        
        return jsonify({
            'message': 'Resume created successfully!',
            'resume_id': new_resume['id']
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Error creating resume: {str(e)}'}), 500

@app.route('/api/resumes', methods=['GET'])
def get_resumes():
    # Check if user is logged in
    if not is_logged_in():
        return jsonify({'message': 'Please login to view resumes'}), 401
    
    current_user_id = get_current_user_id()
    user_resumes = [resume for resume in resumes if resume['user_id'] == current_user_id]
    return jsonify({'resumes': user_resumes}), 200

@app.route('/api/resumes/<resume_id>', methods=['GET'])
def get_resume(resume_id):
    # Check if user is logged in
    if not is_logged_in():
        return jsonify({'message': 'Please login to view resume'}), 401
    
    current_user_id = get_current_user_id()
    
    # Debug: Print request info
    print("=== GET RESUME DEBUG ===")
    print(f"Requested resume ID: {resume_id}")
    print(f"Current user ID: {current_user_id}")
    print(f"Total resumes in memory: {len(resumes)}")
    
    resume = next((r for r in resumes if r['id'] == resume_id and r['user_id'] == current_user_id), None)
    
    if not resume:
        print(f"Resume not found for ID: {resume_id}")
        return jsonify({'message': 'Resume not found'}), 404
    
    print(f"Found resume: {resume}")
    print("=========================")
    return jsonify({'resume': resume}), 200

@app.route('/api/resumes/<resume_id>', methods=['PUT'])
def update_resume(resume_id):
    # Check if user is logged in
    if not is_logged_in():
        return jsonify({'message': 'Please login to update resume'}), 401
    
    current_user_id = get_current_user_id()
    
    resume = next((r for r in resumes if r['id'] == resume_id and r['user_id'] == current_user_id), None)
    
    if not resume:
        return jsonify({'message': 'Resume not found'}), 404
    
    try:
        data = request.get_json()
        
        # Debug: Print received data for update
        print("=== UPDATE RESUME DEBUG ===")
        print(f"Resume ID: {resume_id}")
        print(f"Received data: {data}")
        print(f"Current resume before update: {resume}")
        
        # Update fields if provided - including all personal information
        update_fields = [
            'full_name', 'email', 'phone', 'linkedin', 'address', 'summary',
            'education', 'experience', 'projects', 'skills', 'skill_ratings',
            'profile_picture', 'template_type', 'is_public'
        ]
        
        for field in update_fields:
            if field in data:
                resume[field] = data[field]
                print(f"Updated field '{field}': {data[field]}")
        
        resume['updated_at'] = datetime.utcnow().isoformat()
        
        return jsonify({'message': 'Resume updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error updating resume: {str(e)}'}), 500

@app.route('/api/resumes/<resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    # Check if user is logged in
    if not is_logged_in():
        return jsonify({'message': 'Please login to delete resume'}), 401
    
    current_user_id = get_current_user_id()
    global resumes
    
    resume = next((r for r in resumes if r['id'] == resume_id and r['user_id'] == current_user_id), None)
    
    if not resume:
        return jsonify({'message': 'Resume not found'}), 404
    
    resumes = [r for r in resumes if not (r['id'] == resume_id and r['user_id'] == current_user_id)]
    
    return jsonify({'message': 'Resume deleted successfully'}), 200

# Print and PDF Export Routes
@app.route('/api/resumes/<resume_id>/print', methods=['GET'])
def print_resume(resume_id):
    """Route for printing resume - returns HTML optimized for printing"""
    try:
        # Check if user is logged in
        if not is_logged_in():
            return jsonify({'message': 'Please login to print resume'}), 401
        
        current_user_id = get_current_user_id()
        
        # Debug: Print request info
        print("=== PRINT RESUME DEBUG ===")
        print(f"Print resume ID: {resume_id}")
        print(f"Current user ID: {current_user_id}")
        
        # Find the resume
        resume = next((r for r in resumes if r['id'] == resume_id and r['user_id'] == current_user_id), None)
        
        if not resume:
            print(f"Resume not found for print: {resume_id}")
            return jsonify({'message': 'Resume not found'}), 404
        
        print(f"Found resume for printing: {resume['full_name'] or 'Unnamed'}")
        
        # Prepare skills list
        skills_list = []
        if resume.get('skills'):
            skills_list = [skill.strip() for skill in resume['skills'].split(',') if skill.strip()]
        
        # Generate print-optimized HTML
        print_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Resume - {resume.get('full_name', 'Professional Resume')}</title>
    <style>
        @page {{
            size: A4;
            margin: 0.75in;
        }}
        @media print {{
            body {{ -webkit-print-color-adjust: exact; }}
        }}
        body {{
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #2c3e50;
            margin: 0;
            padding: 0;
        }}
        .resume-header {{
            text-align: center;
            background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
            color: white;
            padding: 25px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .name {{
            font-size: 32pt;
            font-weight: 900;
            margin-bottom: 10px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        .contact-info {{
            font-size: 12pt;
            font-weight: 300;
            opacity: 0.95;
            line-height: 1.4;
        }}
        .contact-item {{
            display: inline-block;
            margin: 0 15px;
        }}
        .section {{
            margin-bottom: 30px;
            page-break-inside: avoid;
        }}
        .section-title {{
            font-size: 18pt;
            font-weight: 900;
            color: #2c3e50;
            background-color: #ecf0f1;
            padding: 15px 20px;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-left: 8px solid #3498db;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .section-content {{
            padding: 0 20px;
            text-align: justify;
            font-size: 11pt;
            line-height: 1.7;
        }}
        .summary-content {{
            font-style: italic;
            color: #34495e;
            border-left: 4px solid #3498db;
            padding: 20px;
            background-color: #f8f9fa;
            margin: 15px 0;
            border-radius: 5px;
        }}
        .skills-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }}
        .skill-item {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 10pt;
            font-weight: 600;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: inline-block;
            margin: 3px;
        }}
        .content-block {{
            margin-bottom: 15px;
        }}
        .print-instruction {{
            text-align: center;
            margin: 20px 0;
            font-size: 14pt;
            color: #7f8c8d;
            display: block;
        }}
        
        /* Fix for long URLs to prevent overflow in print view */
        .contact-info {{
            word-wrap: break-word;
            overflow-wrap: anywhere;
            white-space: normal;
        }}
        
        .contact-item {{
            word-wrap: break-word;
            overflow-wrap: anywhere;
            white-space: normal;
            max-width: 200px;
            vertical-align: top;
        }}
        
        @media print {{
            .print-instruction {{ display: none; }}
            .contact-info {{
                word-wrap: break-word;
                overflow-wrap: anywhere;
                white-space: normal;
            }}
            .contact-item {{
                word-wrap: break-word;
                overflow-wrap: anywhere;
                white-space: normal;
                max-width: 180px;
            }}
        }}
        
        /* Dedicated CSS class for LinkedIn URLs in print view */
        .linkedin-url {{
            word-break: break-all;
            overflow-wrap: break-word;
            white-space: normal;
            display: block;
            margin-top: 5px;
        }}
    </style>
    <script>
        // Auto-trigger print dialog when page loads
        window.onload = function() {{
            setTimeout(function() {{
                window.print();
            }}, 500);
        }};
    </script>
</head>
<body>
    <div class="print-instruction">
        📄 Print dialog will open automatically. If not, press Ctrl+P (Cmd+P on Mac)
    </div>
    
    <!-- Header Section -->
    <div class="resume-header">
        <div class="name">{resume.get('full_name', 'Professional Resume')}</div>
        <div class="contact-info">
            {f'<span class="contact-item">📧 {resume.get("email", "")}' if resume.get('email') else ''}</span>
            {f'<span class="contact-item">📞 {resume.get("phone", "")}' if resume.get('phone') else ''}</span>
            {f'<span class="contact-item">🏠 {resume.get("address", "")}' if resume.get('address') else ''}</span>
            {f'<div class="linkedin-url">🔗 {resume.get("linkedin", "")}' if resume.get('linkedin') else ''}</div>
        </div>
    </div>
    
    <!-- Professional Summary -->
    {f'''
    <div class="section">
        <div class="section-title">🎯 Professional Summary</div>
        <div class="section-content">
            <div class="summary-content">{resume.get('summary', '')}</div>
        </div>
    </div>
    ''' if resume.get('summary') else ''}
    
    <!-- Education -->
    {f'''
    <div class="section">
        <div class="section-title">🎓 Education</div>
        <div class="section-content">
            <div class="content-block">{resume.get('education', '')}</div>
        </div>
    </div>
    ''' if resume.get('education') else ''}
    
    <!-- Experience -->
    {f'''
    <div class="section">
        <div class="section-title">💼 Professional Experience</div>
        <div class="section-content">
            <div class="content-block">{resume.get('experience', '')}</div>
        </div>
    </div>
    ''' if resume.get('experience') else ''}
    
    <!-- Projects -->
    {f'''
    <div class="section">
        <div class="section-title">🚀 Projects Portfolio</div>
        <div class="section-content">
            <div class="content-block">{resume.get('projects', '')}</div>
        </div>
    </div>
    ''' if resume.get('projects') else ''}
    
    <!-- Skills -->
    {f'''
    <div class="section">
        <div class="section-title">🛠️ Core Skills</div>
        <div class="section-content">
            <div class="skills-container">
                {''.join([f'<span class="skill-item">{skill}</span>' for skill in skills_list])}
            </div>
        </div>
    </div>
    ''' if skills_list else ''}
</body>
</html>
        """
        
        print("✅ Print HTML generated successfully")
        print("===========================")
        
        from flask import Response
        return Response(print_html, mimetype='text/html')
        
    except Exception as e:
        print(f"❌ Print resume error: {str(e)}")
        return jsonify({'message': f'Error generating print version: {str(e)}'}), 500

@app.route('/api/resumes/<resume_id>/download', methods=['GET'])
def download_resume_pdf(resume_id):
    """Route for downloading resume as PDF"""
    try:
        from flask import make_response
        from xhtml2pdf import pisa
        from io import BytesIO
        
        # Check authentication
        if not is_logged_in():
            print("❌ Unauthorized PDF download attempt - not logged in")
            return jsonify({'message': 'Please login to download resume'}), 401
        
        current_user_id = get_current_user_id()
        if not current_user_id:
            print("❌ Unauthorized PDF download attempt - no user ID")
            return jsonify({'message': 'Authentication required'}), 401
        
        # Debug: Print request info
        print("=== PDF DOWNLOAD DEBUG ===")
        print(f"PDF resume ID: {resume_id}")
        print(f"Current user ID: {current_user_id}")
        
        # Find the resume
        resume = next((r for r in resumes if r['id'] == resume_id and r['user_id'] == current_user_id), None)
        
        if not resume:
            print(f"Resume not found for PDF: {resume_id}")
            return jsonify({'message': 'Resume not found'}), 404
        
        print(f"Found resume for PDF: {resume.get('full_name', 'Unnamed')}")
        
        # Prepare skills list
        skills_list = []
        if resume.get('skills'):
            skills_list = [skill.strip() for skill in resume['skills'].split(',') if skill.strip()]
        
        # Function to safely truncate extremely long URLs for PDF
        def safe_url_display(url, max_length=60):
            if not url:
                return ''
            if len(url) <= max_length:
                return url
            # For very long URLs, show beginning + ... + end
            # More conservative truncation for PDF
            return f"{url[:max_length-8]}...{url[-5:]}"
        
        # Apply URL truncation to LinkedIn if it's extremely long (more conservative for PDF)
        linkedin_display = safe_url_display(resume.get('linkedin', ''), 60)
        
        # Generate PDF-optimized HTML
        pdf_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @page {{
            size: A4;
            margin: 0.75in;
        }}
        body {{
            font-family: Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #2c3e50;
            margin: 0;
            padding: 0;
        }}
        .resume-header {{
            text-align: center;
            background-color: #3498db;
            color: white;
            padding: 20px;
            margin-bottom: 25px;
        }}
        .name {{
            font-size: 24pt;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .contact-info {{
            font-size: 10pt;
            line-height: 1.4;
            width: 100%;
            max-width: 100%;
            overflow: hidden;
            word-wrap: break-word;
            overflow-wrap: anywhere;
            white-space: normal;
        }}
        .contact-item {{
            display: inline-block;
            margin: 0 10px;
            word-wrap: break-word;
            overflow-wrap: break-word;
            max-width: 150px;
            vertical-align: top;
        }}
        .section {{
            margin-bottom: 20px;
        }}
        .section-title {{
            font-size: 14pt;
            font-weight: bold;
            color: #2c3e50;
            background-color: #ecf0f1;
            padding: 10px 15px;
            margin-bottom: 15px;
            text-transform: uppercase;
            border-left: 5px solid #3498db;
        }}
        .section-content {{
            padding: 0 15px;
            text-align: justify;
            font-size: 10pt;
            line-height: 1.6;
        }}
        .summary-content {{
            font-style: italic;
            color: #34495e;
            border-left: 3px solid #3498db;
            padding: 15px;
            background-color: #f8f9fa;
            margin: 10px 0;
        }}
        .skills-container {{
            margin-top: 10px;
        }}
        .skill-item {{
            background-color: #3498db;
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 9pt;
            font-weight: bold;
            display: inline-block;
            margin: 2px;
        }}
        .content-block {{
            margin-bottom: 10px;
        }}
        
        /* Enhanced CSS class for LinkedIn URLs in PDF with aggressive wrapping */
        .linkedin-url {{
            /* Aggressive text breaking for PDF generators */
            word-break: break-all !important;
            overflow-wrap: break-word !important;
            word-wrap: break-word !important;
            white-space: normal !important;
            
            /* Layout properties */
            display: block;
            margin-top: 5px;
            max-width: 100% !important;
            width: 100%;
            
            /* Text styling */
            font-size: 8pt !important;
            line-height: 1.1 !important;
            
            /* Overflow handling */
            overflow: hidden;
            text-overflow: ellipsis;
            
            /* PDF-specific properties */
            box-sizing: border-box;
            padding: 0;
            margin-left: 0;
            margin-right: 0;
            
            /* Force character-level breaking */
            -webkit-hyphens: auto;
            -moz-hyphens: auto;
            hyphens: auto;
            
            /* Additional PDF generator compatibility */
            overflow-wrap: anywhere !important;
        }}
        
        /* Alternative approach: Multi-line with ellipsis for very long URLs */
        .linkedin-url-multiline {{
            word-break: break-all;
            overflow-wrap: break-word;
            white-space: normal;
            display: block;
            margin-top: 5px;
            max-width: 100%;
            width: 100%;
            font-size: 8pt;
            line-height: 1.1;
            max-height: 2.2em;
            overflow: hidden;
            position: relative;
        }}
    </style>
</head>
<body>
    <!-- Header Section -->
    <div class="resume-header">
        <div class="name">{resume.get('full_name', 'Professional Resume')}</div>
        <div class="contact-info">
            {f'📧 {resume.get("email", "")} ' if resume.get('email') else ''}
            {f'📞 {resume.get("phone", "")} ' if resume.get('phone') else ''}
            {f'🏠 {resume.get("address", "")} ' if resume.get('address') else ''}
            {f'<div class="linkedin-url">🔗 {linkedin_display}</div>' if resume.get('linkedin') else ''}
        </div>
    </div>
    
    <!-- Professional Summary -->
    {f'''
    <div class="section">
        <div class="section-title">Professional Summary</div>
        <div class="section-content">
            <div class="summary-content">{resume.get('summary', '')}</div>
        </div>
    </div>
    ''' if resume.get('summary') else ''}
    
    <!-- Education -->
    {f'''
    <div class="section">
        <div class="section-title">Education</div>
        <div class="section-content">
            <div class="content-block">{resume.get('education', '')}</div>
        </div>
    </div>
    ''' if resume.get('education') else ''}
    
    <!-- Experience -->
    {f'''
    <div class="section">
        <div class="section-title">Professional Experience</div>
        <div class="section-content">
            <div class="content-block">{resume.get('experience', '')}</div>
        </div>
    </div>
    ''' if resume.get('experience') else ''}
    
    <!-- Projects -->
    {f'''
    <div class="section">
        <div class="section-title">Projects Portfolio</div>
        <div class="section-content">
            <div class="content-block">{resume.get('projects', '')}</div>
        </div>
    </div>
    ''' if resume.get('projects') else ''}
    
    <!-- Skills -->
    {f'''
    <div class="section">
        <div class="section-title">Core Skills</div>
        <div class="section-content">
            <div class="skills-container">
                {''.join([f'<span class="skill-item">{skill}</span>' for skill in skills_list])}
            </div>
        </div>
    </div>
    ''' if skills_list else ''}
</body>
</html>
        """
        
        print("Generating PDF from HTML...")
        
        # Generate PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(pdf_html.encode("utf-8")), result)
        
        if pdf.err:
            print(f"❌ PDF generation error: {pdf.err}")
            return jsonify({'message': 'Error generating PDF'}), 500
        
        print("✅ PDF generated successfully")
        print("============================")
        
        # Create response
        response = make_response(result.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{resume.get("full_name", "Resume").replace(" ", "_")}_Resume.pdf"'
        
        return response
        
    except Exception as e:
        print(f"❌ PDF download error: {str(e)}")
        return jsonify({'message': f'Error generating PDF: {str(e)}'}), 500

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
                'applyUrl': 'https://techcorp.example.com/careers/frontend-developer',
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
    from flask import request
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

@app.route('/api/jobs/<job_id>/apply', methods=['POST'])
def apply_for_job(job_id):
    """Endpoint for job applications"""
    from datetime import datetime
    try:
        data = request.get_json()
        job_title = data.get('job_title', 'Unknown Position')
        company = data.get('company', 'Unknown Company')
        
        # Find the job
        job = next((j for j in jobs if j['id'] == job_id), None)
        if not job:
            return jsonify({'message': 'Job not found'}), 404
        
        # Log the application (in a real app, you'd save to database)
        print(f"=== JOB APPLICATION SUBMITTED ===")
        print(f"Job ID: {job_id}")
        print(f"Job Title: {job_title}")
        print(f"Company: {company}")
        print(f"Applied at: {datetime.now()}")
        
        # Check if user is logged in
        user_id = get_current_user_id()
        if user_id:
            user_name = session.get('user_name', 'Unknown User')
            print(f"Applicant: {user_name} (ID: {user_id})")
        else:
            print("Applicant: Anonymous (demo mode)")
        
        print("===================================")
        
        return jsonify({
            'message': f'Thank you for applying to {job_title} at {company}! Your application has been submitted successfully. We will review your application and contact you soon.',
            'status': 'success',
            'job_id': job_id
        }), 200
        
    except Exception as e:
        print(f"Error processing job application: {str(e)}")
        return jsonify({
            'message': 'Thank you for your interest! Your application has been received.',
            'status': 'success'
        }), 200

@app.route('/favicon.ico')
def favicon():
    """Serve favicon or return 204 No Content"""
    return '', 204

if __name__ == '__main__':
    print("Starting Smart Resume in simple mode (no database required)")
    print("Access the application at: http://localhost:8000")
    print("Or from other devices at: http://0.0.0.0:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
