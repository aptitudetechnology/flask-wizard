"""
Miscellaneous Files Generator Module
Generates requirements.txt, README.md, and .env files.
"""
from datetime import datetime

def generate_requirements_content(config: dict) -> str:
    """Generate requirements.txt file content."""
    requirements = [
        "Flask==2.3.3",  # Specific version for consistency
        "gunicorn",  # For production deployment
        "python-dotenv",  # For loading environment variables
    ]
    
    if config['features']['database'] == 'postgres_ready':
        requirements.append("Flask-SQLAlchemy")
        requirements.append("psycopg2-binary")  # PostgreSQL adapter
    
    # Add other common libraries if selected, or if they're generally useful
    if config['features']['features']['user_auth']:
        requirements.append("Werkzeug")  # For password hashing
        # Could add Flask-Login, Flask-WTF if more complex auth is desired
    
    if config['features']['features']['file_uploads']:
        # Consider specific libraries if more robust file handling is needed,
        # otherwise basic Flask handles it.
        pass
    
    if config['features']['features']['background_tasks']:
        requirements.append("celery")
        requirements.append("redis")  # Common broker for Celery
    
    return "\n".join(sorted(requirements))

def generate_readme_content(config: dict) -> str:
    """Generate README.md file content."""
    app_name = config['app_name']
    app_title = config['app_title']
    description = config['description']
    author = config['author']
    current_year = datetime.now().year
    
    # Database description
    db_desc = 'PostgreSQL ready (with SQLite fallback for development)' if config['features']['database'] == 'postgres_ready' else 'SQLite3 (lightweight, file-based database)'
    
    # Feature selections
    user_auth = 'Yes' if config['features']['features']['user_auth'] else 'No'
    file_uploads = 'Yes' if config['features']['features']['file_uploads'] else 'No'
    api_endpoints = 'Yes' if config['features']['features']['api_endpoints'] else 'No'
    background_tasks = 'Yes' if config['features']['features']['background_tasks'] else 'No'
    
    readme_content = '''# ''' + app_title + '''

## Overview

''' + description + '''

This project was generated using the Flask App Generator Wizard.

## Features

* **Modular Structure**: Organized into blueprints for clean code management.
* **Database**: ''' + db_desc + '''
* **Front-end**: Responsive UI with Bootstrap 5 and Bootstrap Icons.
* **Configuration**: Environment variable based configuration using `.env`.
* **Logging**: Basic application logging to console and file.

### Selected Features:
* **User Authentication**: ''' + user_auth + '''
* **File Upload Handling**: ''' + file_uploads + '''
* **REST API Endpoints**: ''' + api_endpoints + '''
* **Background Task Support**: ''' + background_tasks + '''

## Getting Started

### 1. Clone the repository (or extract the generated app)

```bash
# If this was a git repo, you'd clone it
# git clone https://github.com/your-repo/''' + app_name + '''.git
# cd ''' + app_name + '''
```

### 2. Set up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the `.env` file and adjust settings as needed:

```bash
cp .env .env.local  # Optional: create a local copy
# Edit .env with your specific settings
```

### 5. Run the application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
''' + app_name + '''/
├── app.py                 # Main application entry point
├── paths.py              # Path configurations
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
├── routes/              # Route blueprints
│   ├── __init__.py
│   ├── main.py         # Main routes
│   └── api.py          # API routes
├── templates/          # Jinja2 templates
│   ├── base.html
│   ├── dashboard.html
│   └── error.html
├── static/            # Static files
│   ├── css/
│   │   └── custom.css
│   ├── js/
│   │   └── app.js
│   ├── uploads/       # File uploads
│   └── images/        # Static images
├── utils/             # Utility modules
│   ├── __init__.py
│   ├── database.py    # Database utilities
│   ├── helpers.py     # Helper functions
│   └── validators.py  # Input validators
├── data/              # Data storage
│   └── backups/       # Database backups
├── config/            # Configuration files
└── logs/              # Application logs
```

## Configuration

The application uses environment variables for configuration. Key settings in `.env`:

* `FLASK_APP`: Application entry point
* `FLASK_ENV`: Environment (development/production)
* `SECRET_KEY`: Secret key for sessions
* `DATABASE_URL`: Database connection string

## Development

### Adding New Routes

1. Create route functions in `routes/main.py` or `routes/api.py`
2. Add corresponding templates in `templates/`
3. Update navigation in the base template if needed

### Database Operations

Database utilities are available in `utils/database.py`:

```python
from utils.database import get_db_connection, execute_query
```

### Styling

Custom styles go in `static/css/custom.css`. The application uses Bootstrap 5 for base styling.

## Deployment

### Using Gunicorn

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

### Environment Variables for Production

Set these environment variables in production:

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url-here
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created by ''' + author + ''' (''' + str(current_year) + ''')

---

*Generated with Flask App Generator Wizard*
'''
    return readme_content

def generate_env_content(config: dict) -> str:
    """Generate .env file content."""
    app_name = config['app_name']
    
    env_content = '''# Flask Application Configuration
# Generated by Flask App Generator Wizard

# Flask Settings
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True

# Security
SECRET_KEY=''' + app_name.replace('-', '_') + '''_secret_key_change_in_production

# Database Configuration
''' + ('DATABASE_URL=sqlite:///data/' + app_name + '.db' if config['features']['database'] == 'sqlite' else 'DATABASE_URL=postgresql://username:password@localhost:5432/' + app_name) + '''

# Application Settings
APP_NAME=''' + app_name + '''
APP_TITLE="''' + config['app_title'] + '''"

# File Upload Settings
''' + ('UPLOAD_FOLDER=static/uploads\nMAX_CONTENT_LENGTH=16777216  # 16MB max file size' if config['features']['file_uploads'] else '# UPLOAD_FOLDER=static/uploads\n# MAX_CONTENT_LENGTH=16777216  # 16MB max file size') + '''

# Background Tasks (if enabled)
''' + ('CELERY_BROKER_URL=redis://localhost:6379/0\nCELERY_RESULT_BACKEND=redis://localhost:6379/0' if config['features']['features']['background_tasks'] else '# CELERY_BROKER_URL=redis://localhost:6379/0\n# CELERY_RESULT_BACKEND=redis://localhost:6379/0') + '''

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
'''
    return env_content