from flask import Blueprint, request, jsonify, make_response, render_template_string
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Resume, User
from xhtml2pdf import pisa
from io import BytesIO
import json

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/resumes', methods=['POST'])
@jwt_required()
def create_resume():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get user object
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        resume = Resume(
            user=user,
            # Personal Information
            full_name=data.get('full_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            linkedin=data.get('linkedin', ''),
            address=data.get('address', ''),
            summary=data.get('summary', ''),
            # Resume Sections
            education=data.get('education', ''),
            experience=data.get('experience', ''),
            projects=data.get('projects', ''),
            skills=data.get('skills', ''),
            skill_ratings=data.get('skill_ratings', {}),
            # Additional Fields
            profile_picture=data.get('profile_picture', ''),
            template_type=data.get('template_type', 'modern'),
            is_public=data.get('is_public', False)
        )
        
        resume.save()
        
        return jsonify({
            'message': 'Resume created successfully',
            'resume_id': str(resume.id)
        }), 201
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@resume_bp.route('/resumes', methods=['GET'])
@jwt_required()
def get_user_resumes():
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        resumes = Resume.objects(user=user)
        
        resumes_data = []
        for resume in resumes:
            resumes_data.append({
                'id': str(resume.id),
                # Personal Information
                'full_name': resume.full_name or '',
                'email': resume.email or '',
                'phone': resume.phone or '',
                'linkedin': resume.linkedin or '',
                'address': resume.address or '',
                'summary': resume.summary or '',
                # Resume Sections
                'education': resume.education or '',
                'experience': resume.experience or '',
                'projects': resume.projects or '',
                'skills': resume.skills or '',
                'skill_ratings': resume.skill_ratings or {},
                # Additional Fields
                'profile_picture': resume.profile_picture or '',
                'template_type': resume.template_type or 'modern',
                'is_public': resume.is_public or False,
                # Timestamps
                'created_at': resume.created_at.isoformat(),
                'updated_at': resume.updated_at.isoformat()
            })
        
        return jsonify({'resumes': resumes_data}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@resume_bp.route('/resumes/<resume_id>', methods=['GET'])
@jwt_required()
def get_resume(resume_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        resume = Resume.objects(id=resume_id, user=user).first()
        
        if not resume:
            return jsonify({'message': 'Resume not found'}), 404
        
        return jsonify({
            'resume': {
                'id': str(resume.id),
                # Personal Information
                'full_name': resume.full_name or '',
                'email': resume.email or '',
                'phone': resume.phone or '',
                'linkedin': resume.linkedin or '',
                'address': resume.address or '',
                'summary': resume.summary or '',
                # Resume Sections
                'education': resume.education or '',
                'experience': resume.experience or '',
                'projects': resume.projects or '',
                'skills': resume.skills or '',
                'skill_ratings': resume.skill_ratings or {},
                # Additional Fields
                'profile_picture': resume.profile_picture or '',
                'template_type': resume.template_type or 'modern',
                'is_public': resume.is_public or False,
                # Timestamps
                'created_at': resume.created_at.isoformat(),
                'updated_at': resume.updated_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@resume_bp.route('/resumes/<resume_id>', methods=['PUT'])
@jwt_required()
def update_resume(resume_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        resume = Resume.objects(id=resume_id, user=user).first()
        
        if not resume:
            return jsonify({'message': 'Resume not found'}), 404
        
        data = request.get_json()
        
        # Update Personal Information fields
        if 'full_name' in data:
            resume.full_name = data['full_name']
        if 'email' in data:
            resume.email = data['email']
        if 'phone' in data:
            resume.phone = data['phone']
        if 'linkedin' in data:
            resume.linkedin = data['linkedin']
        if 'address' in data:
            resume.address = data['address']
        if 'summary' in data:
            resume.summary = data['summary']
            
        # Update Resume Sections
        if 'education' in data:
            resume.education = data['education']
        if 'experience' in data:
            resume.experience = data['experience']
        if 'projects' in data:
            resume.projects = data['projects']
        if 'skills' in data:
            resume.skills = data['skills']
        if 'skill_ratings' in data:
            resume.skill_ratings = data['skill_ratings']
            
        # Update Additional Fields
        if 'profile_picture' in data:
            resume.profile_picture = data['profile_picture']
        if 'template_type' in data:
            resume.template_type = data['template_type']
        if 'is_public' in data:
            resume.is_public = data['is_public']
        
        resume.save()
        
        return jsonify({'message': 'Resume updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@resume_bp.route('/resumes/<resume_id>', methods=['DELETE'])
@jwt_required()
def delete_resume(resume_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        resume = Resume.objects(id=resume_id, user=user).first()
        
        if not resume:
            return jsonify({'message': 'Resume not found'}), 404
        
        resume.delete()
        
        return jsonify({'message': 'Resume deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@resume_bp.route('/resumes/<resume_id>/download', methods=['GET'])
@jwt_required()
def download_resume_pdf(resume_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        resume = Resume.objects(id=resume_id, user=user).first()
        
        if not resume:
            return jsonify({'message': 'Resume not found'}), 404
        
        # Generate Enhanced PDF HTML template with Bold Headers
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @page {
                    size: A4;
                    margin: 0.75in;
                }
                body {
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    font-size: 10pt;
                    line-height: 1.5;
                    color: #2c3e50;
                    margin: 0;
                    padding: 0;
                }
                .resume-header {
                    text-align: center;
                    background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
                    color: white;
                    padding: 20px;
                    margin-bottom: 25px;
                    border-radius: 8px;
                }
                .name {
                    font-size: 28pt;
                    font-weight: 900;
                    margin-bottom: 8px;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                }
                .contact-info {
                    font-size: 11pt;
                    font-weight: 300;
                    opacity: 0.95;
                    line-height: 1.4;
                }
                .contact-item {
                    display: inline-block;
                    margin: 0 10px;
                }
                .section {
                    margin-bottom: 25px;
                    page-break-inside: avoid;
                }
                .section-title {
                    font-size: 16pt;
                    font-weight: 900;
                    color: #2c3e50;
                    background-color: #ecf0f1;
                    padding: 12px 15px;
                    margin-bottom: 15px;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    border-left: 6px solid #3498db;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
                .section-content {
                    padding: 0 15px;
                    text-align: justify;
                    font-size: 10pt;
                    line-height: 1.6;
                }
                .summary-content {
                    font-style: italic;
                    color: #34495e;
                    border-left: 3px solid #3498db;
                    padding-left: 15px;
                    background-color: #f8f9fa;
                    padding: 15px;
                    margin: 10px 0;
                }
                .skills-container {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-top: 10px;
                }
                .skill-item {
                    background: linear-gradient(135deg, #3498db, #2980b9);
                    color: white;
                    padding: 6px 14px;
                    border-radius: 20px;
                    font-size: 9pt;
                    font-weight: 600;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    display: inline-block;
                    margin: 2px;
                }
                .content-block {
                    margin-bottom: 12px;
                }
                .highlight {
                    font-weight: 700;
                    color: #2c3e50;
                }
            </style>
        </head>
        <body>
            <!-- Header Section with Personal Information -->
            <div class="resume-header">
                <div class="name">{{ full_name or user_name }}</div>
                <div class="contact-info">
                    {% if resume_email or user_email %}
                    <span class="contact-item">📧 {{ resume_email or user_email }}</span>
                    {% endif %}
                    {% if phone %}
                    <span class="contact-item">📞 {{ phone }}</span>
                    {% endif %}
                    {% if address %}
                    <span class="contact-item">🏠 {{ address }}</span>
                    {% endif %}
                    {% if linkedin %}
                    <br><span class="contact-item">🔗 {{ linkedin }}</span>
                    {% endif %}
                </div>
            </div>
            
            <!-- Professional Summary Section -->
            {% if summary %}
            <div class="section">
                <div class="section-title">🎯 Professional Summary</div>
                <div class="section-content">
                    <div class="summary-content">{{ summary }}</div>
                </div>
            </div>
            {% endif %}
            
            <!-- Education Section -->
            {% if education %}
            <div class="section">
                <div class="section-title">🎓 Education</div>
                <div class="section-content">
                    <div class="content-block">{{ education }}</div>
                </div>
            </div>
            {% endif %}
            
            <!-- Professional Experience Section -->
            {% if experience %}
            <div class="section">
                <div class="section-title">💼 Professional Experience</div>
                <div class="section-content">
                    <div class="content-block">{{ experience }}</div>
                </div>
            </div>
            {% endif %}
            
            <!-- Projects Section -->
            {% if projects %}
            <div class="section">
                <div class="section-title">🚀 Projects Portfolio</div>
                <div class="section-content">
                    <div class="content-block">{{ projects }}</div>
                </div>
            </div>
            {% endif %}
            
            <!-- Skills Section -->
            {% if skills %}
            <div class="section">
                <div class="section-title">🛠️ Core Skills</div>
                <div class="section-content">
                    <div class="skills-container">
                        {% for skill in skills_list %}
                        <span class="skill-item">{{ skill }}</span>
                        {% endfor %}
                    </div>
                </div>
            </div>
            {% endif %}
        </body>
        </html>
        """
        
        # Prepare template variables
        skills_list = []
        if resume.skills:
            skills_list = [skill.strip() for skill in resume.skills.split(',') if skill.strip()]
        
        html_content = render_template_string(html_template,
            # User defaults
            user_name=user.name,
            user_email=user.email,
            # Resume personal information
            full_name=resume.full_name,
            resume_email=resume.email,
            phone=resume.phone,
            linkedin=resume.linkedin,
            address=resume.address,
            summary=resume.summary,
            # Resume sections
            education=resume.education,
            experience=resume.experience,
            projects=resume.projects,
            skills=resume.skills,
            skills_list=skills_list
        )
        
        # Generate PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode("utf-8")), result)
        
        if pdf.err:
            return jsonify({'message': 'Error generating PDF'}), 500
        
        # Create response
        response = make_response(result.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{user.name}_Resume.pdf"'
        
        return response
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
