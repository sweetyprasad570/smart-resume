#!/usr/bin/env python3
"""
Simple test app to verify login page and PDF functionality without database issues
"""

from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'

# Mock data for testing
mock_users = {
    'test@example.com': {
        'id': '1',
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'  # In real app, this would be hashed
    }
}

mock_resumes = {
    '1': {
        'id': '1',
        'education': 'Bachelor of Computer Science - University of Technology',
        'experience': 'Software Developer at Tech Corp (2020-2023)\nJunior Developer at StartupXYZ (2019-2020)',
        'projects': 'Smart Resume Builder - Web application for creating professional resumes\nE-commerce Platform - Full-stack web application',
        'skills': 'Python, JavaScript, React, Flask, MongoDB, HTML, CSS',
        'created_at': '2024-01-15T10:30:00Z',
        'updated_at': '2024-01-15T10:30:00Z'
    }
}

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

@app.route('/api/auth/login', methods=['POST'])
def mock_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = mock_users.get(email)
        if user and user['password'] == password:
            return jsonify({
                'message': 'Login successful',
                'access_token': 'mock-access-token-12345',
                'refresh_token': 'mock-refresh-token-67890',
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
        return jsonify({'message': str(e)}), 500

@app.route('/api/resumes', methods=['GET'])
def mock_get_resumes():
    return jsonify({
        'resumes': list(mock_resumes.values())
    }), 200

@app.route('/api/resumes/<resume_id>')
def mock_get_resume(resume_id):
    resume = mock_resumes.get(resume_id)
    if resume:
        return jsonify({'resume': resume}), 200
    else:
        return jsonify({'message': 'Resume not found'}), 404

@app.route('/api/resumes/<resume_id>/download')
def mock_download_resume(resume_id):
    """Test the PDF download functionality"""
    try:
        from xhtml2pdf import pisa
        from flask import make_response
        from io import BytesIO
        
        resume = mock_resumes.get(resume_id)
        if not resume:
            return jsonify({'message': 'Resume not found'}), 404
        
        user = mock_users['test@example.com']  # Mock user
        
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
                }}
                .skills-list {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                }}
                .skill-item {{
                    background-color: #ecf0f1;
                    padding: 4px 12px;
                    border-radius: 15px;
                    font-size: 9pt;
                    color: #2c3e50;
                    border: 1px solid #bdc3c7;
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
                <div class="section-content">{resume.get('education', '')}</div>
            </div>
            
            <div class="section">
                <div class="section-title">Experience</div>
                <div class="section-content">{resume.get('experience', '')}</div>
            </div>
            
            <div class="section">
                <div class="section-title">Projects</div>
                <div class="section-content">{resume.get('projects', '')}</div>
            </div>
            
            <div class="section">
                <div class="section-title">Skills</div>
                <div class="section-content">
                    <div class="skills-list">
                        {' '.join([f'<span class="skill-item">{skill.strip()}</span>' for skill in resume.get('skills', '').split(',') if skill.strip()])}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Generate PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_template.encode("utf-8")), result)
        
        if pdf.err:
            return jsonify({'message': 'Error generating PDF'}), 500
        
        # Create response
        response = make_response(result.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{user["name"]}_Resume.pdf"'
        
        return response
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    print("Starting Smart Resume Test Application...")
    print("Login with: test@example.com / password123")
    print("Access at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
