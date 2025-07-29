"""
Miscellaneous Files Generator Module
Generates requirements.txt, README.md, and .env files.
"""

from datetime import datetime

def generate_requirements_content(config: dict) -> str:
    """Generate requirements.txt file content."""
    requirements = [
        "Flask==2.3.3", # Specific version for consistency
        "gunicorn",     # For production deployment
        "python-dotenv", # For loading environment variables
    ]

    if config['features']['database'] == 'postgres_ready':
        requirements.append("Flask-SQLAlchemy")
        requirements.append("psycopg2-binary") # PostgreSQL adapter

    # Add other common libraries if selected, or if they're generally useful
    if config['features']['user_auth']:
        requirements.append("Werkzeug") # For password hashing
        # Could add Flask-Login, Flask-WTF if more complex auth is desired

    if config['features']['file_uploads']:
        # Consider specific libraries if more robust file handling is needed,
        # otherwise basic Flask handles it.
        pass

    if config['features']['background_tasks']:
        requirements.append("celery")
        requirements.append("redis") # Common broker for Celery

    return "\n".join(sorted(requirements))

def generate_readme_content(config: dict) -> str:
    """Generate README.md file content."""
    app_name = config['app_name']
    app_title = config['app_title']
    description = config['description']
    author = config['author']
    current_year = datetime.now().year

    readme_content = f'''# {app_title}

## Overview
{description}

This project was generated using the Flask App Generator Wizard.

## Features
* **Modular Structure**: Organized into blueprints for clean code management.
* **Database**: {'PostgreSQL ready (with SQLite fallback for development)' if config['features']['database'] == 'postgres_ready' else 'SQLite3 (lightweight, file-based database)'}
* **Front-end**: Responsive UI with Bootstrap 5 and Bootstrap Icons.
* **Configuration**: Environment variable based configuration using `.env`.
* **Logging**: Basic application logging to console and file.

### Selected Features:
* **User Authentication**: {'Yes' if config['features']['user_auth'] else 'No'}
* **File Upload Handling**: {'Yes' if config['features']['file_uploads'] else 'No'}
* **REST API Endpoints**: {'Yes' if config['features']['api_endpoints'] else 'No'}
* **Background Task Support**: {'Yes' if config['features']['background_tasks'] else 'No'}

## Getting Started

### 1. Clone the repository (or extract the generated app)
```bash
# If this was a git repo, you'd clone it
# git clone [https://github.com/your-repo/](https://github.com/your-repo/){app_name}.git
# cd {app_name}