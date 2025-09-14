#!/usr/bin/env python3
"""
Test script to verify Resume page fixes
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpass123"

def test_resume_functionality():
    """Test the resume functionality end-to-end"""
    session = requests.Session()
    
    print("🚀 Testing Resume Page Fixes")
    print("=" * 50)
    
    # Step 1: Test API status
    print("\n1️⃣ Testing API status...")
    try:
        response = session.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            print("✅ API is running")
        else:
            print("❌ API is not responding correctly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return
    
    # Step 2: Test login (which will create demo user)
    print("\n2️⃣ Testing login functionality...")
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Login successful (demo user created)")
            login_result = response.json()
            print(f"   User: {login_result.get('user', {}).get('name')}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 3: Test getting resumes (should return empty list initially)
    print("\n3️⃣ Testing GET /api/resumes (should be empty initially)...")
    try:
        response = session.get(f"{BASE_URL}/api/resumes")
        if response.status_code == 200:
            resumes_data = response.json()
            resumes = resumes_data.get('resumes', [])
            print(f"✅ GET /api/resumes works - found {len(resumes)} resumes")
            if len(resumes) == 0:
                print("   ✅ Empty state correctly handled")
        else:
            print(f"❌ GET /api/resumes failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ GET /api/resumes error: {e}")
        return
    
    # Step 4: Test creating a resume
    print("\n4️⃣ Testing POST /api/resumes (create new resume)...")
    resume_data = {
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1 (555) 123-4567",
        "linkedin": "https://linkedin.com/in/johndoe",
        "address": "San Francisco, CA",
        "summary": "Experienced software developer with expertise in Python and JavaScript",
        "education": "Bachelor of Computer Science, MIT, 2020",
        "experience": "Software Developer at TechCorp (2020-2023)",
        "projects": "Built e-commerce platform, Real-time chat application",
        "skills": "Python, JavaScript, React, Node.js, MongoDB"
    }
    
    try:
        response = session.post(f"{BASE_URL}/api/resumes", json=resume_data)
        if response.status_code == 201:
            print("✅ POST /api/resumes works - resume created")
            create_result = response.json()
            resume_id = create_result.get('resume_id')
            print(f"   Resume ID: {resume_id}")
        else:
            print(f"❌ POST /api/resumes failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ POST /api/resumes error: {e}")
        return
    
    # Step 5: Test getting resumes again (should now have 1 resume)
    print("\n5️⃣ Testing GET /api/resumes (should have 1 resume now)...")
    try:
        response = session.get(f"{BASE_URL}/api/resumes")
        if response.status_code == 200:
            resumes_data = response.json()
            resumes = resumes_data.get('resumes', [])
            print(f"✅ GET /api/resumes works - found {len(resumes)} resumes")
            if len(resumes) == 1:
                print("   ✅ Resume creation and retrieval working correctly")
                resume = resumes[0]
                print(f"   Resume: {resume.get('full_name')} ({resume.get('email')})")
            else:
                print(f"   ⚠️ Expected 1 resume, got {len(resumes)}")
        else:
            print(f"❌ GET /api/resumes failed: {response.status_code}")
    except Exception as e:
        print(f"❌ GET /api/resumes error: {e}")
    
    # Step 6: Test frontend page accessibility
    print("\n6️⃣ Testing frontend /resumes page accessibility...")
    try:
        response = session.get(f"{BASE_URL}/resumes")
        if response.status_code == 200 and "My Resumes" in response.text:
            print("✅ /resumes page loads successfully")
            if "Create New Resume" in response.text:
                print("   ✅ 'Create New Resume' button is present")
        else:
            print(f"❌ /resumes page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ /resumes page error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Resume functionality test completed!")
    print("\nTo manually test:")
    print(f"1. Go to {BASE_URL}/login")
    print(f"2. Login with: {TEST_EMAIL} / {TEST_PASSWORD}")
    print(f"3. Go to {BASE_URL}/resumes")
    print("4. Click 'Create New Resume' button - modal should open")
    print("5. Fill form and save - should see resume in list")

if __name__ == "__main__":
    test_resume_functionality()
