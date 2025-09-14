from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Job, User

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    try:
        # Check if user is admin
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user or not user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        
        data = request.get_json()
        
        job = Job(
            job_title=data['job_title'],
            company=data['company'],
            required_skills=data.get('required_skills', [])
        )
        
        job.save()
        
        return jsonify({
            'message': 'Job created successfully',
            'job_id': str(job.id)
        }), 201
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        jobs = Job.objects()
        jobs_data = []
        
        for job in jobs:
            jobs_data.append({
                'id': str(job.id),
                'job_title': job.job_title,
                'company': job.company,
                'required_skills': job.required_skills or [],
                'created_at': job.created_at.isoformat(),
                'updated_at': job.updated_at.isoformat()
            })
        
        return jsonify({'jobs': jobs_data}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@jobs_bp.route('/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    try:
        job = Job.objects(id=job_id).first()
        
        if not job:
            return jsonify({'message': 'Job not found'}), 404
        
        return jsonify({
            'job': {
                'id': str(job.id),
                'job_title': job.job_title,
                'company': job.company,
                'required_skills': job.required_skills or [],
                'created_at': job.created_at.isoformat(),
                'updated_at': job.updated_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@jobs_bp.route('/jobs/<job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    try:
        # Check if user is admin
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user or not user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        
        job = Job.objects(id=job_id).first()
        
        if not job:
            return jsonify({'message': 'Job not found'}), 404
        
        data = request.get_json()
        
        if 'job_title' in data:
            job.job_title = data['job_title']
        if 'company' in data:
            job.company = data['company']
        if 'required_skills' in data:
            job.required_skills = data['required_skills']
        
        job.save()
        
        return jsonify({'message': 'Job updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@jobs_bp.route('/jobs/<job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    try:
        # Check if user is admin
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user or not user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        
        job = Job.objects(id=job_id).first()
        
        if not job:
            return jsonify({'message': 'Job not found'}), 404
        
        job.delete()
        
        return jsonify({'message': 'Job deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
