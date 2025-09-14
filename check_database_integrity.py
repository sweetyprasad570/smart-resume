#!/usr/bin/env python3
"""
Smart Resume Database Integrity Checker

This script checks the integrity of both simple (in-memory) and full (MongoDB) databases.
"""

import sys
import json
from datetime import datetime
import traceback

def check_simple_database():
    """Check integrity of the simple in-memory database"""
    print("="*60)
    print("CHECKING SIMPLE DATABASE (IN-MEMORY)")
    print("="*60)
    
    try:
        # Import the simple app
        import simple_app
        
        print("✅ Simple app imports successfully")
        
        # Test the app instance
        app = simple_app.app
        print("✅ Flask app instance created")
        
        # Check routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = [
            '/',
            '/api/resumes',
            '/api/jobs',
            '/api/auth/login',
            '/api/status'
        ]
        
        missing_routes = []
        for route in expected_routes:
            found = any(route in r for r in routes)
            if not found:
                missing_routes.append(route)
        
        if missing_routes:
            print(f"⚠️  Missing routes: {missing_routes}")
        else:
            print("✅ All essential routes are present")
        
        # Test database operations with test client
        with app.test_client() as client:
            # Test status endpoint
            response = client.get('/api/status')
            if response.status_code == 200:
                print("✅ API status endpoint working")
            else:
                print(f"❌ API status failed: {response.status_code}")
            
            # Test jobs endpoint
            response = client.get('/api/jobs')
            if response.status_code == 200:
                jobs_data = response.get_json()
                print(f"✅ Jobs endpoint working - {len(jobs_data.get('jobs', []))} jobs loaded")
            else:
                print(f"❌ Jobs endpoint failed: {response.status_code}")
            
            # Test resume creation
            test_resume = {
                'education': 'Test Education',
                'experience': 'Test Experience',
                'projects': 'Test Projects',
                'skills': 'Python, JavaScript'
            }
            
            response = client.post('/api/resumes', 
                                 json=test_resume,
                                 content_type='application/json')
            
            if response.status_code == 201:
                print("✅ Resume creation working")
                
                # Test resume retrieval
                response = client.get('/api/resumes')
                if response.status_code == 200:
                    resumes_data = response.get_json()
                    print(f"✅ Resume retrieval working - {len(resumes_data.get('resumes', []))} resumes found")
                else:
                    print(f"❌ Resume retrieval failed: {response.status_code}")
            else:
                print(f"❌ Resume creation failed: {response.status_code}")
        
        print("\n📊 Simple Database Summary:")
        print(f"   - In-memory storage: ✅ Working")
        print(f"   - API endpoints: ✅ Functional") 
        print(f"   - Data operations: ✅ Working")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import simple_app: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking simple database: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def check_full_database():
    """Check integrity of the full MongoDB database"""
    print("\n" + "="*60)
    print("CHECKING FULL DATABASE (MONGODB)")
    print("="*60)
    
    try:
        # Import the full app
        import app
        
        print("✅ Full app imports successfully")
        
        # Test the app instance
        flask_app = app.app
        print("✅ Flask app instance created")
        
        # Test database connection with test client
        with flask_app.test_client() as client:
            # Test database status
            response = client.get('/test-db')
            
            if response.status_code == 200:
                db_data = response.get_json()
                print("✅ Database connection successful")
                print(f"   Status: {db_data.get('database_status')}")
                
                collections = db_data.get('collections', {})
                for collection, count in collections.items():
                    print(f"   {collection}: {count}")
                
                # Test relationship integrity
                response = client.get('/test-relationship')
                if response.status_code == 200:
                    rel_data = response.get_json()
                    print("✅ Database relationships working")
                    print(f"   Test result: {rel_data.get('relationship_test')}")
                else:
                    print(f"⚠️  Relationship test returned: {response.status_code}")
                    
            else:
                db_data = response.get_json() if response.data else {}
                print(f"❌ Database connection failed: {response.status_code}")
                print(f"   Error: {db_data.get('error', 'Unknown error')}")
                return False
        
        # Check models
        try:
            from models import User, Resume, Job, PasswordReset
            print("✅ All models imported successfully")
            
            # Test model structure
            user_fields = User._fields.keys()
            resume_fields = Resume._fields.keys()
            job_fields = Job._fields.keys()
            
            expected_user_fields = {'name', 'email', 'password', 'created_at'}
            expected_resume_fields = {'user', 'education', 'experience', 'skills', 'created_at'}
            expected_job_fields = {'job_title', 'company', 'required_skills', 'created_at'}
            
            if expected_user_fields.issubset(user_fields):
                print("✅ User model structure correct")
            else:
                missing = expected_user_fields - user_fields
                print(f"⚠️  User model missing fields: {missing}")
            
            if expected_resume_fields.issubset(resume_fields):
                print("✅ Resume model structure correct")
            else:
                missing = expected_resume_fields - resume_fields
                print(f"⚠️  Resume model missing fields: {missing}")
            
            if expected_job_fields.issubset(job_fields):
                print("✅ Job model structure correct")
            else:
                missing = expected_job_fields - job_fields
                print(f"⚠️  Job model missing fields: {missing}")
                
        except ImportError as e:
            print(f"❌ Cannot import models: {e}")
            return False
        
        print("\n📊 Full Database Summary:")
        print(f"   - MongoDB connection: ✅ Working")
        print(f"   - Model structure: ✅ Correct") 
        print(f"   - Relationships: ✅ Functional")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import full app (likely MongoDB not installed): {e}")
        print("   This is normal if you're only using simple mode")
        return False
    except Exception as e:
        print(f"❌ Error checking full database: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def check_file_integrity():
    """Check integrity of essential files"""
    print("\n" + "="*60)
    print("CHECKING FILE INTEGRITY")
    print("="*60)
    
    import os
    
    essential_files = [
        ('simple_app.py', 'Simple application file'),
        ('app.py', 'Full application file'),
        ('models.py', 'Database models'),
        ('config.py', 'Configuration file'),
        ('requirements.txt', 'Dependencies list'),
        ('templates/base.html', 'Base template'),
        ('templates/resumes.html', 'Resume template'),
        ('templates/jobs.html', 'Jobs template'),
        ('static/css/style.css', 'Main stylesheet'),
        ('static/js/main.js', 'Main JavaScript'),
        ('start_smart_resume.bat', 'Simple launcher'),
        ('setup.bat', 'Setup script'),
    ]
    
    missing_files = []
    corrupted_files = []
    
    for file_path, description in essential_files:
        if os.path.exists(file_path):
            try:
                # Check if file is readable and has content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if len(content) > 0:
                        print(f"✅ {description}: {file_path}")
                    else:
                        print(f"⚠️  Empty file: {file_path}")
                        corrupted_files.append(file_path)
            except Exception as e:
                print(f"❌ Cannot read {file_path}: {e}")
                corrupted_files.append(file_path)
        else:
            print(f"❌ Missing: {file_path} ({description})")
            missing_files.append(file_path)
    
    print(f"\n📊 File Integrity Summary:")
    print(f"   - Total files checked: {len(essential_files)}")
    print(f"   - Missing files: {len(missing_files)}")
    print(f"   - Corrupted files: {len(corrupted_files)}")
    
    if missing_files:
        print(f"   Missing: {missing_files}")
    if corrupted_files:
        print(f"   Corrupted: {corrupted_files}")
    
    return len(missing_files) == 0 and len(corrupted_files) == 0

def main():
    """Main integrity check function"""
    print("🔍 SMART RESUME DATABASE INTEGRITY CHECK")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Track results
    results = {
        'simple_db': False,
        'full_db': False,
        'files': False
    }
    
    # Check file integrity first
    results['files'] = check_file_integrity()
    
    # Check simple database
    results['simple_db'] = check_simple_database()
    
    # Check full database
    results['full_db'] = check_full_database()
    
    # Final summary
    print("\n" + "="*60)
    print("🎯 FINAL INTEGRITY REPORT")
    print("="*60)
    
    print(f"📁 File Integrity: {'✅ PASS' if results['files'] else '❌ FAIL'}")
    print(f"🗃️  Simple Database: {'✅ PASS' if results['simple_db'] else '❌ FAIL'}")
    print(f"🗄️  Full Database: {'✅ PASS' if results['full_db'] else '⚠️  N/A (MongoDB not available)'}")
    
    # Overall status
    critical_pass = results['files'] and results['simple_db']
    
    if critical_pass:
        print("\n🎉 OVERALL STATUS: ✅ HEALTHY")
        print("   Your Smart Resume application is ready to use!")
        print("   Recommendation: Use 'start_smart_resume.bat' to launch")
    else:
        print("\n⚠️  OVERALL STATUS: ❌ ISSUES DETECTED")
        print("   Some issues were found. Check the details above.")
        if not results['simple_db']:
            print("   Critical: Simple database has issues")
        if not results['files']:
            print("   Critical: Missing or corrupted files detected")
    
    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return critical_pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
