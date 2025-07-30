"""
Core App Generator Module
Generates the main app.py file and the paths.py configuration.
"""

from datetime import datetime
import json

def generate_paths_file_content(config: dict) -> str:
    """Generate paths.py file content for centralized path management."""
    app_title = config['app_title']
    paths_code = f'''"""
Path Configuration for {app_title}
Centralized path management using pathlib
"""

from pathlib import Path

# Base application directory
BASE_DIR = Path(__file__).parent.resolve()

# Core directories
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
LOGS_DIR = BASE_DIR / "logs"
ROUTES_DIR = BASE_DIR / "routes"
UTILS_DIR = BASE_DIR / "utils"

# Static subdirectories
CSS_DIR = STATIC_DIR / "css"
JS_DIR = STATIC_DIR / "js"
UPLOADS_DIR = STATIC_DIR / "uploads"
IMAGES_DIR = STATIC_DIR / "images"

# Database paths
DATABASE_DIR = BASE_DIR / "data"
DATABASE_PATH = DATABASE_DIR / "database.db"
BACKUP_DIR = DATABASE_DIR / "backups"

# Configuration paths
ENV_FILE = BASE_DIR / ".env"
CONFIG_DIR = BASE_DIR / "config"

# Log file paths
APP_LOG = LOGS_DIR / "app.log"
ERROR_LOG = LOGS_DIR / "error.log"
ACCESS_LOG = LOGS_DIR / "access.log"

def ensure_directories():
    """Ensure all necessary directories exist"""
    directories = [
        LOGS_DIR,
        UPLOADS_DIR,
        IMAGES_DIR,
        DATABASE_DIR,
        BACKUP_DIR,
        CONFIG_DIR
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def get_upload_path(filename: str) -> Path:
    """Get safe upload path for a filename"""
    # Sanitize filename and return full path
    # Assuming sanitize_filename is available in utils.helpers
    from utils.helpers import sanitize_filename
    safe_filename = sanitize_filename(filename)
    return UPLOADS_DIR / safe_filename

def get_log_path(log_type: str) -> Path:
    """Get log file path by type"""
    log_paths = {{
        'app': APP_LOG,
        'error': ERROR_LOG,
        'access': ACCESS_LOG
    }}
    return log_paths.get(log_type, APP_LOG)

# Initialize directories on import
ensure_directories()
'''
    return paths_code

def generate_main_app_content(config: dict) -> str:
    """Generate the main Flask application file content."""
    app_title = config['app_title']
    description = config['description']
    author = config['author']
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    use_postgres = config['features']['database'] == 'postgres_ready'
    use_user_auth = config['features']['user_auth']

    # Handle nav_items JSON serialization properly
    nav_items_json = json.dumps(config['nav_items'], indent=8)

    app_code = f'''"""
{app_title}
{description}

Author: {author}
Generated: {current_time}
"""

import os
import logging
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime

# Import blueprints from the routes package
from routes import register_blueprints

# Import utilities
from utils.database import init_db, get_db_connection, get_setting
from utils.helpers import format_datetime # For general template use
import json

# Path configuration
from paths import BASE_DIR, LOGS_DIR

{'from flask_sqlalchemy import SQLAlchemy' if use_postgres else ''}

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
app.config['APPLICATION_NAME'] = '{app_title}'
app.config['DATABASE_PATH'] = BASE_DIR / 'data' / 'database.db' # SQLite path
{'app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", f"sqlite:///' + '{app.config["DATABASE_PATH"]}")' if use_postgres else ''}
{'app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False' if use_postgres else ''}

# Initialize extensions
{'db = SQLAlchemy(app)' if use_postgres else ''}

# Logging setup
LOGS_DIR.mkdir(parents=True, exist_ok=True) # Ensure logs directory exists
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / 'app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Register Blueprints
register_blueprints(app)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 Not Found: {{request.path}}")
    return render_template('error.html', error="Page not found", code=404), 404

@app.errorhandler(500)
def server_error(error):
    logger.exception(f"500 Internal Server Error: {{error}}")
    return render_template('error.html', error="Internal server error", code=500), 500

# Template context processors
@app.context_processor
def inject_globals():
    """Inject global variables and functions into all templates"""
    nav_items_data = [...]  # actual list of nav items
    return dict(
    nav_items=nav_items_data,
    app_title=app.config['APPLICATION_NAME'],
    current_year=datetime.now().year,
    get_setting=get_setting,
    format_datetime=format_datetime
    )

if __name__ == '__main__':
    with app.app_context():
        # Initialize database tables
        init_db()
        {'db.create_all()' if use_postgres else ''} # For SQLAlchemy models

    debug = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))

    logger.info(f"Starting {{app.config.get('APPLICATION_NAME', '{app_title}')}} on http://0.0.0.0:{{port}}")
    app.run(debug=debug, port=port, host='0.0.0.0')
'''
    return app_code