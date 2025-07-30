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
    
    features = config.get('features', {})
    database = features.get('database', 'sqlite')
    if database == 'postgres_ready':
        requirements.append("Flask-SQLAlchemy")
        requirements.append("psycopg2-binary")  # PostgreSQL adapter
    
    # Add other common libraries if selected, or if they're generally useful
    nested = features.get('features', {})
    user_auth = features.get('user_auth', nested.get('user_auth', False))
    if user_auth:
        requirements.append("Werkzeug")  # For password hashing
        # Could add Flask-Login, Flask-WTF if more complex auth is desired
    
    file_uploads = features.get('file_uploads', nested.get('file_uploads', False))
    if file_uploads:
        # Consider specific libraries if more robust file handling is needed,
        # otherwise basic Flask handles it.
        pass
    
    background_tasks = features.get('background_tasks', nested.get('background_tasks', False))
    if background_tasks:
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

    features = config.get('features', {})
    nested = features.get('features', {})
    database = features.get('database', 'sqlite')
    user_auth = features.get('user_auth', nested.get('user_auth', False))
    file_uploads = features.get('file_uploads', nested.get('file_uploads', False))
    api_endpoints = features.get('api_endpoints', nested.get('api_endpoints', False))
    background_tasks = features.get('background_tasks', nested.get('background_tasks', False))

    # Database description
    db_desc = 'PostgreSQL ready (with SQLite fallback for development)' if database == 'postgres_ready' else 'SQLite3 (lightweight, file-based database)'

    # Feature selections
    user_auth_str = 'Yes' if user_auth else 'No'
    file_uploads_str = 'Yes' if file_uploads else 'No'
    api_endpoints_str = 'Yes' if api_endpoints else 'No'
    background_tasks_str = 'Yes' if background_tasks else 'No'

    readme_content = (
        f"# {app_title}\n\n"
        "## Overview\n\n"
        f"{description}\n\n"
        "This project was generated using the Flask App Generator Wizard.\n\n"
        "## Features\n\n"
        "* **Modular Structure**: Organized into blueprints for clean code management.\n"
        f"* **Database**: {db_desc}\n"
        "* **Front-end**: Responsive UI with Bootstrap 5 and Bootstrap Icons.\n"
        "* **Configuration**: Environment variable based configuration using `.env`.\n"
        "* **Logging**: Basic application logging to console and file.\n\n"
        "### Selected Features:\n"
        f"* **User Authentication**: {user_auth_str}\n"
        f"* **File Upload Handling**: {file_uploads_str}\n"
        f"* **REST API Endpoints**: {api_endpoints_str}\n"
        f"* **Background Task Support**: {background_tasks_str}\n\n"
        "## Getting Started\n\n"
        "### 1. Clone the repository (or extract the generated app)\n\n"
        "```bash\n"
        f"# If this was a git repo, you'd clone it\n# git clone https://github.com/your-repo/{app_name}.git\n# cd {app_name}\n"
        "```\n\n"
        "### 2. Set up a virtual environment\n\n"
        "```bash\n"
        "python3 -m venv venv\n"
        "source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`\n"
        "```\n\n"
        "### 3. Install dependencies\n\n"
        "```bash\n"
        "pip install -r requirements.txt\n"
        "```\n\n"
        "### 4. Set up environment variables\n\n"
        "Copy the `.env` file and adjust settings as needed:\n\n"
        "```bash\n"
        "cp .env .env.local  # Optional: create a local copy\n"
        "# Edit .env with your specific settings\n"
        "```\n\n"
        "### 5. Run the application\n\n"
        "```bash\n"
        "python app.py\n"
        "```\n\n"
        "The application will be available at `http://localhost:5000`\n\n"
        "## Project Structure\n\n"
        f"{app_name}/\n"
        "├── app.py                 # Main application entry point\n"
        "├── paths.py              # Path configurations\n"
        "├── requirements.txt      # Python dependencies\n"
        "├── .env                 # Environment variables\n"
        "├── routes/              # Route blueprints\n"
        "│   ├── __init__.py\n"
        "│   ├── main.py         # Main routes\n"
        "│   └── api.py          # API routes\n"
        "├── templates/          # Jinja2 templates\n"
        "│   ├── base.html\n"
        "│   ├── dashboard.html\n"
        "│   └── error.html\n"
        "├── static/            # Static files\n"
        "│   ├── css/\n"
        "│   │   └── custom.css\n"
        "│   ├── js/\n"
        "│   │   └── app.js\n"
        "│   ├── uploads/       # File uploads\n"
        "│   └── images/        # Static images\n"
        "├── utils/             # Utility modules\n"
        "│   ├── __init__.py\n"
        "│   ├── database.py    # Database utilities\n"
        "│   ├── helpers.py     # Helper functions\n"
        "│   └── validators.py  # Input validators\n"
        "├── data/              # Data storage\n"
        "│   └── backups/       # Database backups\n"
        "├── config/            # Configuration files\n"
        "└── logs/              # Application logs\n"
        "```\n\n"
        "## Configuration\n\n"
        "The application uses environment variables for configuration. Key settings in `.env`:\n\n"
        "* `FLASK_APP`: Application entry point\n"
        "* `FLASK_ENV`: Environment (development/production)\n"
        "* `SECRET_KEY`: Secret key for sessions\n"
        "* `DATABASE_URL`: Database connection string\n\n"
        "## Development\n\n"
        "### Adding New Routes\n\n"
        "1. Create route functions in `routes/main.py` or `routes/api.py`\n"
        "2. Add corresponding templates in `templates/`\n"
        "3. Update navigation in the base template if needed\n\n"
        "### Database Operations\n\n"
        "Database utilities are available in `utils/database.py`:\n\n"
        "```python\n"
        "from utils.database import get_db_connection, execute_query\n"
        "```\n\n"
        "### Styling\n\n"
        "Custom styles go in `static/css/custom.css`. The application uses Bootstrap 5 for base styling.\n\n"
        "## Deployment\n\n"
        "### Using Gunicorn\n\n"
        "```bash\n"
        "gunicorn --bind 0.0.0.0:8000 app:app\n"
        "```\n\n"
        "### Environment Variables for Production\n\n"
        "Set these environment variables in production:\n\n"
        "```bash\n"
        "FLASK_ENV=production\n"
        "SECRET_KEY=your-secret-key-here\n"
        "DATABASE_URL=your-database-url-here\n"
        "```\n\n"
        "## Contributing\n\n"
        "1. Fork the repository\n"
        "2. Create a feature branch (`git checkout -b feature/amazing-feature`)\n"
        "3. Commit your changes (`git commit -m 'Add amazing feature'`)\n"
        "4. Push to the branch (`git push origin feature/amazing-feature`)\n"
        "5. Open a Pull Request\n\n"
        "## License\n\n"
        "This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.\n\n"
        "## Author\n\n"
        f"Created by {author} ({current_year})\n\n"
        "---\n\n"
        "*Generated with Flask App Generator Wizard*\n"
    )
    return readme_content

def generate_env_content(config: dict) -> str:
    """Generate .env file content."""
    app_name = config['app_name']
    features = config.get('features', {})
    nested = features.get('features', {})
    database = features.get('database', 'sqlite')
    file_uploads = features.get('file_uploads', nested.get('file_uploads', False))
    background_tasks = features.get('background_tasks', nested.get('background_tasks', False))

    env_content = (
        "# Flask Application Configuration\n"
        "# Generated by Flask App Generator Wizard\n\n"
        "# Flask Settings\n"
        "FLASK_APP=app.py\n"
        "FLASK_ENV=development\n"
        "FLASK_DEBUG=True\n\n"
        "# Security\n"
        f"SECRET_KEY={app_name.replace('-', '_')}_secret_key_change_in_production\n\n"
        "# Database Configuration\n"
        + (
            f"DATABASE_URL=sqlite:///data/{app_name}.db\n" if database == "sqlite" else f"DATABASE_URL=postgresql://username:password@localhost:5432/{app_name}\n"
        )
        + "\n# Application Settings\n"
        f"APP_NAME={app_name}\n"
        f'APP_TITLE="{config.get("app_title", app_name)}"\n\n'
        "# File Upload Settings\n"
        + (
            "UPLOAD_FOLDER=static/uploads\nMAX_CONTENT_LENGTH=16777216  # 16MB max file size\n" if file_uploads else "# UPLOAD_FOLDER=static/uploads\n# MAX_CONTENT_LENGTH=16777216  # 16MB max file size\n"
        )
        + "\n# Background Tasks (if enabled)\n"
        + (
            "CELERY_BROKER_URL=redis://localhost:6379/0\nCELERY_RESULT_BACKEND=redis://localhost:6379/0\n" if background_tasks else "# CELERY_BROKER_URL=redis://localhost:6379/0\n# CELERY_RESULT_BACKEND=redis://localhost:6379/0\n"
        )
        + "\n# Logging\n"
        "LOG_LEVEL=INFO\n"
        "LOG_FILE=logs/app.log\n"
    )
    return env_content

def generate_settings_content(config: dict) -> str:
    """Generate settings.py file content."""
    app_name = config['app_name']
    features = config.get('features', {})
    nested = features.get('features', {})
    database = features.get('database', 'sqlite')
    user_auth = features.get('user_auth', nested.get('user_auth', False))
    file_uploads = features.get('file_uploads', nested.get('file_uploads', False))
    background_tasks = features.get('background_tasks', nested.get('background_tasks', False))

    settings_content = f'''"""
Flask Application Settings

This module contains configuration settings for the Flask application.
Generated by Flask App Generator Wizard for {config.get('app_title', app_name)}.
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class."""
    
    # Basic Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or '{app_name.replace("-", "_")}_secret_key_change_in_production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 'on']
    TESTING = False
    
    # Application settings
    APP_NAME = os.environ.get('APP_NAME') or '{app_name}'
    APP_TITLE = os.environ.get('APP_TITLE') or '{config.get("app_title", app_name)}'
    
    # Database settings'''

    if database == 'sqlite':
        settings_content += f'''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///data/{app_name}.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False'''
    else:  # postgres_ready
        settings_content += f'''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://username:password@localhost:5432/{app_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {{
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }}'''

    if file_uploads:
        settings_content += '''
    
    # File upload settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'static/uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16777216))  # 16MB default'''

    if user_auth:
        settings_content += '''
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax''''

    if background_tasks:
        settings_content += '''
    
    # Celery settings
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True'''

    settings_content += '''
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DEVELOPMENT = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_SSL_STRICT = True
    
    # Performance settings
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(hours=1)


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {{
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}}


def get_config():
    """Get configuration based on environment."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
'''

    return settings_content