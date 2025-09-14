from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Resume

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """Get current user profile data"""
    try:
        current_user_id = get_jwt_identity()
        user = User.objects(id=current_user_id).first()
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        resume_count = Resume.objects(user=user).count()
        
        return jsonify({
            'user': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
                'is_admin': user.is_admin,
                'created_at': user.created_at.isoformat(),
                'resume_count': resume_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = User.objects()
        users_data = []
        
        for user in users:
            users_data.append({
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
                'is_admin': user.is_admin,
                'created_at': user.created_at.isoformat()
            })
        
        return jsonify({'users': users_data}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        user = User.objects(id=user_id).first()
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        resume_count = Resume.objects(user=user).count()
        
        return jsonify({
            'user': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
                'is_admin': user.is_admin,
                'created_at': user.created_at.isoformat(),
                'resume_count': resume_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Only allow users to update their own profile or admin users
        current_user = User.objects(id=current_user_id).first()
        if current_user_id != user_id and not current_user.is_admin:
            return jsonify({'message': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            # Check if email is already taken by another user
            existing_user = User.objects(email=data['email']).first()
            if existing_user and str(existing_user.id) != user_id:
                return jsonify({'message': 'Email already in use'}), 400
            user.email = data['email']
        
        user.save()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
                'is_admin': user.is_admin
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
