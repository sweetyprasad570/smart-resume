from flask import Flask, jsonify, render_template
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from models import User, Resume, Job, PasswordReset
from config import Config
from routes.auth import auth_bp
from routes.user import user_bp
from routes.resume import resume_bp
from routes.jobs import jobs_bp
from routes.main import main_bp

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Add current_user context processor for templates
    @app.context_processor
    def inject_current_user():
        from flask import session, request
        from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
        
        current_user = None
        user_data = None
        
        try:
            # Try JWT authentication first
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                try:
                    current_user = User.objects(id=user_id).first()
                    if current_user:
                        user_data = {
                            'id': str(current_user.id),
                            'name': current_user.name,
                            'email': current_user.email
                        }
                except Exception as e:
                    print(f"Error fetching user from JWT: {e}")
        except Exception:
            # JWT not available or invalid, try session-based auth
            pass
        
        # Fallback to session-based authentication (for simple_app.py compatibility)
        if not current_user and 'user_id' in session:
            user_data = {
                'id': session.get('user_id'),
                'name': session.get('user_name', 'User'),
                'email': session.get('user_email', '')
            }
            current_user = True  # Simplified boolean for template
        
        return dict(
            current_user=current_user or (user_data is not None),
            user_data=user_data
        )

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'msg': 'Token has expired'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'msg': 'Invalid token'}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'msg': 'Authorization token required'}), 401

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(resume_bp, url_prefix='/api')
    app.register_blueprint(jobs_bp, url_prefix='/api')
    
    # Main routes
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/favicon.ico')
    def favicon():
        from flask import send_from_directory
        return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    @app.route('/api/status')
    def api_status():
        return jsonify({
            "message": "Smart Resume API is running!",
            "status": "success",
            "endpoints": {
                "home": "/",
                "api_status": "/api/status",
                "test_db": "/test-db"
            }
        })
    
    @app.route('/health')
    def health():
        return jsonify({
            "status": "healthy",
            "database": "connected"
        })
    
    @app.route('/test-db')
    def test_db():
        try:
            # Check collections by counting documents
            user_count = User.objects.count()
            resume_count = Resume.objects.count()
            job_count = Job.objects.count()
            password_reset_count = PasswordReset.objects.count()

            return jsonify({
                "database_status": "working",
                "collections": {
                    "users": f"{user_count} documents",
                    "resumes": f"{resume_count} documents",
                    "jobs": f"{job_count} documents",
                    "password_resets": f"{password_reset_count} documents"
                },
                "message": "Database is working fine!"
            })
        except Exception as e:
            return jsonify({
                "database_status": "error",
                "error": str(e)
            }), 500
    
    @app.route('/test-relationship')
    def test_relationship():
        try:
            # Create a test user and resume to verify relationship
            test_user = User(name="Test User", email="test@example.com")
            test_user.set_password("testpass")
            test_user.save()

            test_resume = Resume(
                user=test_user,
                education="Test Education",
                experience="Test Experience",
                skills="Python, Flask"
            )
            test_resume.save()

            # Test the relationship
            user_resumes = Resume.objects(user=test_user)
            resume_user = User.objects(id=test_user.id).first()

            return jsonify({
                "relationship_test": "success",
                "user_id": str(test_user.id),
                "user_name": test_user.name,
                "resume_count": user_resumes.count(),
                "resume_owner": resume_user.name if resume_user else "None",
                "message": "User-Resume relationship working!"
            })
        except Exception as e:
            return jsonify({
                "relationship_test": "error",
                "error": str(e)
            }), 500
    
    @app.route('/favicon.ico')
    def favicon():
        """Serve favicon or return 204 No Content"""
        return '', 204
    
    return app

# Create app instance for import
app = create_app()

if __name__ == '__main__':
    print("Starting Smart Resume application...")
    print("Access the application at: http://localhost:5000")
    print("Or from other devices at: http://0.0.0.0:5000")
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Error starting the application: {e}")
        print("Try running simple_app.py for a version without database dependencies")
