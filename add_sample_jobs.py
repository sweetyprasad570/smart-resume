#!/usr/bin/env python3
"""
Script to add sample jobs to the database for testing the modal functionality
"""
from app import create_app
from models import Job
from datetime import datetime, timedelta

def add_sample_jobs():
    """Add sample jobs to the database"""
    app = create_app()
    
    with app.app_context():
        # Check if jobs already exist
        existing_jobs = Job.objects.count()
        print(f"Existing jobs in database: {existing_jobs}")
        
        if existing_jobs > 0:
            print("Jobs already exist, skipping sample data creation")
            return
        
        # Create sample jobs
        sample_jobs = [
            {
                'job_title': 'Frontend Developer',
                'company': 'TechCorp Inc.',
                'required_skills': ['JavaScript', 'React', 'HTML', 'CSS']
            },
            {
                'job_title': 'Python Developer',
                'company': 'DataSoft Solutions',
                'required_skills': ['Python', 'Django', 'PostgreSQL', 'API Development']
            },
            {
                'job_title': 'Full Stack Developer',
                'company': 'Innovation Labs',
                'required_skills': ['JavaScript', 'Python', 'React', 'Node.js', 'MongoDB']
            },
            {
                'job_title': 'DevOps Engineer',
                'company': 'CloudTech Systems',
                'required_skills': ['Docker', 'Kubernetes', 'AWS', 'Python', 'Linux']
            },
            {
                'job_title': 'Data Scientist',
                'company': 'AI Innovations',
                'required_skills': ['Python', 'Machine Learning', 'Pandas', 'Scikit-learn', 'SQL']
            }
        ]
        
        # Add jobs to database
        for job_data in sample_jobs:
            job = Job(**job_data)
            job.save()
            print(f"Added job: {job.job_title} at {job.company}")
        
        print(f"\n✅ Successfully added {len(sample_jobs)} sample jobs!")
        
        # Verify jobs were added
        total_jobs = Job.objects.count()
        print(f"Total jobs in database: {total_jobs}")

if __name__ == "__main__":
    print("🚀 Adding sample jobs to database...")
    add_sample_jobs()
    print("✨ Sample jobs creation completed!")
