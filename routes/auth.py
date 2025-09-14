from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import db, User, PasswordReset
from datetime import datetime, timedelta
import random
import string

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # Check if user already exists
        if User.objects(email=data['email']).first():
            return jsonify({'message': 'Email already registered'}), 400

        # Create new user
        user = User(
            name=data['name'],
            email=data['email']
        )
        user.set_password(data['password'])  # Properly hash password
        user.save()

        return jsonify({
            'message': 'User registered successfully',
            'user_id': str(user.id)
        }), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.objects(email=data['email']).first()

        if user and user.check_password(data['password']):
            tokens = user.generate_tokens()
            response = jsonify({
                'message': 'Login successful',
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token'],
                'user': {
                    'id': str(user.id),
                    'name': user.name,
                    'email': user.email,
                    'is_admin': user.is_admin
                }
            })
            # Set httpOnly cookies for page requests
            response.set_cookie('access_token', tokens['access_token'], max_age=3600, httponly=True, samesite='Lax')
            response.set_cookie('refresh_token', tokens['refresh_token'], max_age=30*24*3600, httponly=True, samesite='Lax')
            return response, 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({
            'user': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
                'is_admin': user.is_admin,
                'created_at': user.created_at.isoformat()
            }
        }), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        response = jsonify({'message': 'Logged out successfully'})
        # Clear httpOnly cookies
        response.set_cookie('access_token', '', expires=0)
        response.set_cookie('refresh_token', '', expires=0)
        return response, 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
