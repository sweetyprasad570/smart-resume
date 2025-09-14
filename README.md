# Smart Resume Application

A Flask-based web application for creating and managing resumes with job matching capabilities.

## 🚀 Quick Start (One-Click Launch)

### Method 1: Easy Setup & Launch (Recommended)

1. **First Time Setup**: Double-click `setup.bat` to install all dependencies
2. **Start Application**: Double-click `start_smart_resume.bat` to launch the app
3. **Open Browser**: Go to http://localhost:5000

### Method 2: Manual Launch

If you're experiencing database connection issues or want to test the application quickly:

```bash
python simple_app.py
```

This will start the application in demo mode with in-memory storage.

## Full Application (With MongoDB)

For the complete application with persistent storage:

```bash
python app.py
```

## Accessing the Application

Once started, you can access the application at:
- **Local Access**: http://localhost:5000
- **Network Access**: http://0.0.0.0:5000 (accessible from other devices on your network)

## Available Pages

- **Home**: `/` - Landing page
- **Login**: `/login` - User authentication
- **Register**: `/register` - User registration  
- **Dashboard**: `/dashboard` - Main user dashboard
- **Resumes**: `/resumes` - Create and manage resumes
- **Jobs**: `/jobs` - View and manage job applications

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Resumes
- `GET /api/resumes` - Get all user resumes
- `POST /api/resumes` - Create new resume
- `GET /api/resumes/<id>` - Get specific resume
- `PUT /api/resumes/<id>` - Update resume
- `DELETE /api/resumes/<id>` - Delete resume

### System
- `GET /api/status` - API status check
- `GET /health` - Health check
- `GET /test-db` - Database connection test

## Troubleshooting

### "Site can't be reached" Error

1. **Use Simple Mode**: Run `python simple_app.py` instead of `python app.py`
2. **Check Port**: Make sure port 5000 isn't being used by another application
3. **Firewall**: Check if Windows Firewall is blocking the connection
4. **Try Different URLs**:
   - http://localhost:5000
   - http://127.0.0.1:5000
   - http://0.0.0.0:5000

### "Failed to create resume" Error

This is usually due to database connection issues. Solutions:

1. **Use Simple Mode**: Run `python simple_app.py` for testing
2. **Install MongoDB**: The full app requires MongoDB to be installed and running
3. **Check Database Connection**: Visit `/test-db` to verify database connectivity

### Authentication Issues

In simple mode, the app uses demo authentication:
- Any login credentials will work
- All users share the same demo session
- Perfect for testing the UI and basic functionality

## Dependencies

Required Python packages (install with `pip install -r requirements.txt`):
- Flask==2.3.3
- flask-mongoengine==1.0.0
- Flask-JWT-Extended==4.5.3
- bcrypt==4.0.1
- Flask-CORS==4.0.0
- And others listed in requirements.txt

## 📁 Batch Files (Windows)

### Available Launchers:
- **`setup.bat`** - One-time setup to install all Python dependencies
- **`start_smart_resume.bat`** - Start simple mode (recommended, no database required)
- **`start_full_app.bat`** - Start full mode (requires MongoDB database)

### Usage:
1. **First time**: Double-click `setup.bat` to install dependencies
2. **Regular use**: Double-click `start_smart_resume.bat` to start the app
3. **Advanced**: Use `start_full_app.bat` if you have MongoDB installed

## Development Notes

- `simple_app.py` - Lightweight version for testing (no database required)
- `app.py` - Full application with MongoDB integration  
- `setup.bat` - Automated dependency installation
- `start_smart_resume.bat` - Simple app launcher
- `start_full_app.bat` - Full app launcher
- Frontend uses Bootstrap 5 for styling
- API uses JWT tokens for authentication (in full mode)
- All static files (CSS/JS) are served from `/static/` directory
