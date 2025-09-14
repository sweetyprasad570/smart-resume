from flask import Blueprint, render_template, redirect, url_for, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, decode_token
from models import User
import functools
from flask import request as flask_request

main_bp = Blueprint('main', __name__)

def login_required_page(f):
    """Decorator to require login for page routes"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Try to verify JWT from Authorization header or from cookie
            try:
                verify_jwt_in_request(optional=False)
            except Exception:
                # Try to verify token from cookie manually
                token = flask_request.cookies.get('access_token')
                if not token:
                    raise Exception("No token found")
                # Manually decode and set identity in context
                decoded = decode_token(token)  # Will raise if invalid
                # Set the identity in flask_jwt_extended context
                # from flask_jwt_extended import _set_request_context
                # _set_request_context(identity=decoded['sub'])
                # Instead, just check if token is valid and set current_user_id manually
                current_user_id = decoded['sub']
            else:
                current_user_id = get_jwt_identity()
            if current_user_id:
                return f(*args, **kwargs)
        except Exception as e:
            print(f"Authentication error: {e}")
        return redirect(url_for('main.login_page'))
    return decorated_function

@main_bp.route('/dashboard')
@login_required_page
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/login')
def login_page():
    # Always show login page, no redirects
    return render_template('login.html')

@main_bp.route('/register')
def register_page():
    return render_template('register.html')

@main_bp.route('/profile')
@login_required_page
def profile_page():
    return render_template('profile.html')

@main_bp.route('/view-profile')
@login_required_page
def view_profile_page():
    return render_template('view_profile.html')

@main_bp.route('/edit-profile')
@login_required_page
def edit_profile_page():
    return render_template('edit_profile.html')

@main_bp.route('/resumes')
@login_required_page
def resumes_page():
    return render_template('resumes.html')

@main_bp.route('/jobs')
def jobs_page():
    return render_template('jobs.html')

@main_bp.route('/logout', methods=['POST'])
def logout():
    from flask import session, redirect, url_for
    # Clear session data
    session.clear()
    return redirect(url_for('home'))
 