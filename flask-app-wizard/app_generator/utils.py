"""
Utilities Generator Module
Generates __init__.py, database.py, helpers.py, and validators.py for the utils package.
"""

def generate_utils_init_content() -> str:
    """Generate __init__.py file content for the utils package."""
    utils_init = '''"""
Utilities package for helper functions and common operations
"""

from .database import get_db_connection, init_db, get_setting, set_setting, log_activity
from .helpers import log_user_action, format_datetime, sanitize_filename, get_file_size_human, truncate_text, generate_unique_filename
from .validators import validate_email, validate_filename
'''
    return utils_init

def generate_database_utils_content(config: dict) -> str:
    """Generate database.py file content."""
    app_title = config['app_title']
    use_user_auth = config['features']['user_auth']
    db_type = config['features']['database']

    if db_type == 'sqlite':
        db_connection_code = '''
import sqlite3
import logging
from pathlib import Path
from paths import DATABASE_PATH, DATABASE_DIR

logger = logging.getLogger(__name__)

def get_db_connection():
    """Get SQLite database connection with row factory"""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True) # Ensure database directory exists
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
'''
        init_db_code = f'''
def init_db():
    """Initialize SQLite database with all required tables"""
    conn = get_db_connection()

    try:
        # App settings table
        conn.execute(\'\'\'
            CREATE TABLE IF NOT EXISTS app_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        \'\'\')

        # Activity log table
        conn.execute(\'\'\'
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                user_ip TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        \'\'\')

        {'# User authentication table' if use_user_auth else ''}
        {"conn.execute('''"
        "    CREATE TABLE IF NOT EXISTS users ("
        "        id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "        username TEXT UNIQUE NOT NULL,"
        "        email TEXT UNIQUE NOT NULL,"
        "        password_hash TEXT NOT NULL,"
        "        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
        "        last_login TIMESTAMP,"
        "        is_active BOOLEAN DEFAULT 1,"
        "        is_admin BOOLEAN DEFAULT 0"
        "    )"
        "''')" if use_user_auth else ''}

        # Insert default settings
        default_settings = [
            ('app_name', '{app_title}', 'Application name'),
            ('version', '1.0.0', 'Application version'),
            ('maintenance_mode', 'false', 'Maintenance mode status')
        ]

        for key, value, description in default_settings:
            conn.execute(\'\'\'
                INSERT OR IGNORE INTO app_settings (key, value, description)
                VALUES (?, ?, ?)
            \'\'\', (key, value, description))

        conn.commit()
        logger.info("Database initialized successfully")

    except Exception as e:
        logger.error(f"Database initialization failed: {{e}}")
        conn.rollback()
        raise
    finally:
        conn.close()

def get_setting(key: str, default=None):
    """Get application setting by key"""
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT value FROM app_settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        return result['value'] if result else default
    finally:
        conn.close()

def set_setting(key: str, value: str, description: str = None):
    """Set application setting"""
    conn = get_db_connection()
    try:
        conn.execute(\'\'\'
            INSERT OR REPLACE INTO app_settings (key, value, description, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        \'\'\', (key, value, description))
        conn.commit()
        logger.info(f"Setting updated: {{key}} = {{value}}")
    finally:
        conn.close()

def log_activity(action: str, user_ip: str = None, details: str = None):
    """Log user activity to the database"""
    conn = get_db_connection()
    try:
        conn.execute(\'\'\'
            INSERT INTO activity_log (action, user_ip, details)
            VALUES (?, ?, ?)
        \'\'\', (action, user_ip, details))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to log activity: {{e}}")
    finally:
        conn.close()
'''
    elif db_type == 'postgres_ready':
        db_connection_code = '''
import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

logger = logging.getLogger(__name__)

# Base for declarative models (if using Flask-SQLAlchemy, this would be `db.Model`)
Base = declarative_base()

# Define models here if not using Flask-SQLAlchemy directly in app.py
class AppSetting(Base):
    __tablename__ = 'app_settings'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<AppSetting(key='{self.key}', value='{self.value}')>"

class ActivityLog(Base):
    __tablename__ = 'activity_log'
    id = Column(Integer, primary_key=True)
    action = Column(String, nullable=False)
    user_ip = Column(String)
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ActivityLog(action='{self.action}', timestamp='{self.timestamp}')>"

''' + ('''
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(username='{self.username}')>"
''' if use_user_auth else '') + '''

_engine = None
_Session = None

def _get_engine():
    global _engine
    if _engine is None:
        db_url = os.environ.get("DATABASE_URL", "sqlite:///data/database.db")
        _engine = create_engine(db_url)
    return _engine

def get_db_connection():
    """Get SQLAlchemy session"""
    global _Session
    if _Session is None:
        engine = _get_engine()
        _Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _Session()

def init_db():
    """Initialize database tables for PostgreSQL/SQLite"""
    engine = _get_engine()
    Base.metadata.create_all(bind=engine) # Create tables if they don't exist

    session = get_db_connection()
    try:
        # Insert default settings if they don't exist
        default_settings = [
            ('app_name', '''' + app_title + '''', 'Application name'),
            ('version', '1.0.0', 'Application version'),
            ('maintenance_mode', 'false', 'Maintenance mode status')
        ]
        for key, value, description in default_settings:
            if not session.query(AppSetting).filter_by(key=key).first():
                setting = AppSetting(key=key, value=value, description=description)
                session.add(setting)
        session.commit()
        logger.info("Database initialized successfully (PostgreSQL/SQLite ready)")
    except Exception as e:
        logger.error(f"Database initialization failed: {{e}}")
        session.rollback()
        raise
    finally:
        session.close()

def get_setting(key: str, default=None):
    """Get application setting by key"""
    session = get_db_connection()
    try:
        setting = session.query(AppSetting).filter_by(key=key).first()
        return setting.value if setting else default
    finally:
        session.close()

def set_setting(key: str, value: str, description: str = None):
    """Set application setting"""
    session = get_db_connection()
    try:
        setting = session.query(AppSetting).filter_by(key=key).first()
        if setting:
            setting.value = value
            if description: setting.description = description
        else:
            setting = AppSetting(key=key, value=value, description=description)
            session.add(setting)
        session.commit()
        logger.info(f"Setting updated: {{key}} = {{value}}")
    except Exception as e:
        logger.error(f"Failed to set setting {{key}}: {{e}}")
        session.rollback()
    finally:
        session.close()

def log_activity(action: str, user_ip: str = None, details: str = None):
    """Log user activity to the database"""
    session = get_db_connection()
    try:
        log_entry = ActivityLog(action=action, user_ip=user_ip, details=details)
        session.add(log_entry)
        session.commit()
    except Exception as e:
        logger.error(f"Failed to log activity: {{e}}")
        session.rollback()
    finally:
        session.close()
'''
    else: # Fallback to SQLite if something unexpected happens
        db_connection_code = '''
import sqlite3
import logging
from pathlib import Path
from paths import DATABASE_PATH, DATABASE_DIR

logger = logging.getLogger(__name__)

def get_db_connection():
    """Get SQLite database connection with row factory"""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
'''
        init_db_code = f'''
def init_db():
    """Initialize SQLite database with all required tables"""
    conn = get_db_connection()

    try:
        conn.execute(\'\'\'
            CREATE TABLE IF NOT EXISTS app_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        \'\'\')
        conn.execute(\'\'\'
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                user_ip TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        \'\'\')
        {'# User authentication table' if use_user_auth else ''}
        {"conn.execute('''"
        "    CREATE TABLE IF NOT EXISTS users ("
        "        id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "        username TEXT UNIQUE NOT NULL,"
        "        email TEXT UNIQUE NOT NULL,"
        "        password_hash TEXT NOT NULL,"
        "        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
        "        last_login TIMESTAMP,"
        "        is_active BOOLEAN DEFAULT 1,"
        "        is_admin BOOLEAN DEFAULT 0"
        "    )"
        "''')" if use_user_auth else ''}

        default_settings = [
            ('app_name', '{app_title}', 'Application name'),
            ('version', '1.0.0', 'Application version'),
            ('maintenance_mode', 'false', 'Maintenance mode status')
        ]
        for key, value, description in default_settings:
            conn.execute(\'\'\'
                INSERT OR IGNORE INTO app_settings (key, value, description)
                VALUES (?, ?, ?)
            \'\'\', (key, value, description))
        conn.commit()
        logger.info("Database initialized successfully (default SQLite)")

    except Exception as e:
        logger.error(f"Database initialization failed: {{e}}")
        conn.rollback()
        raise
    finally:
        conn.close()

def get_setting(key: str, default=None):
    """Get application setting by key"""
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT value FROM app_settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        return result['value'] if result else default
    finally:
        conn.close()

def set_setting(key: str, value: str, description: str = None):
    """Set application setting"""
    conn = get_db_connection()
    try:
        conn.execute(\'\'\'
            INSERT OR REPLACE INTO app_settings (key, value, description, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        \'\'\', (key, value, description))
        conn.commit()
        logger.info(f"Setting updated: {{key}} = {{value}}")
    finally:
        conn.close()

def log_activity(action: str, user_ip: str = None, details: str = None):
    """Log user activity to the database"""
    conn = get_db_connection()
    try:
        conn.execute(\'\'\'
            INSERT INTO activity_log (action, user_ip, details)
            VALUES (?, ?, ?)
        \'\'\', (action, user_ip, details))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to log activity: {{e}}")
    finally:
        conn.close()
'''
    return db_connection_code + init_db_code

def generate_helpers_utils_content() -> str:
    """Generate helpers.py file content."""
    helpers_utils = '''"""
General helper functions
"""

import re
import logging
from datetime import datetime
from pathlib import Path
from utils.database import log_activity # Correct import path

logger = logging.getLogger(__name__)

def log_user_action(action: str, user_ip: str = None, details: str = None):
    """Log user action to database"""
    try:
        log_activity(action, user_ip, details)
    except Exception as e:
        logger.error(f"Failed to log user action: {{e}}")

def format_datetime(dt, format_str="%Y-%m-%d %H:%M:%S"):
    """Format datetime object or string to string"""
    if isinstance(dt, str):
        try:
            # Attempt to parse string to datetime object first, then format
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00')) # Handle 'Z' for UTC
        except ValueError:
            pass # Keep as string if parsing fails, or handle error
    if not isinstance(dt, datetime):
        # If it's still not a datetime object (e.g., failed parsing or None), return empty string
        return ""
    return dt.strftime(format_str)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace unsafe characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    # Limit length (e.g., to 255 characters for many file systems)
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        max_name_len = 255 - (len(ext) + 1 if ext else 0)
        filename = name[:max_name_len] + ('.' + ext if ext else '')
    return filename

def get_file_size_human(size_bytes: int) -> str:
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f}{size_names[i]}"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def generate_unique_filename(original_filename: str, upload_dir: Path) -> str:
    """Generate unique filename to avoid conflicts"""
    base_name = sanitize_filename(original_filename)
    name, ext = base_name.rsplit('.', 1) if '.' in base_name else (base_name, '')

    counter = 1
    unique_name = base_name

    while (upload_dir / unique_name).exists():
        unique_name = f"{name}_{counter}" + (f".{ext}" if ext else "")
        counter += 1

    return unique_name

# Example for API Key validation - needs implementation
def validate_api_key(api_key: str) -> bool:
    """
    Validate an API key.
    In a real application, this would check against a database of valid API keys.
    """
    # For demonstration, a hardcoded key. Replace with proper lookup.
    VALID_API_KEY = "your_super_secret_api_key_123"
    return api_key == VALID_API_KEY
'''
    return helpers_utils

def generate_validators_utils_content() -> str:
    """Generate validators.py file content."""
    validators_utils = '''"""
Validation utility functions
"""

import re
from pathlib import Path

def validate_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_filename(filename: str) -> bool:
    """
    Validate filename for basic safety.
    Checks for characters typically disallowed or problematic in filenames.
    """
    # Disallow path traversal, null bytes, and common forbidden characters
    if ".." in filename or "/" in filename or "\\\\" in filename or "\\\\0" in filename:
        return False
    # Basic check for empty or excessively long names (though sanitize_filename handles length)
    if not filename or len(filename) > 255:
        return False
    # Regex to allow alphanumeric, periods, hyphens, underscores
    pattern = r"^[a-zA-Z0-9_.-]+$"
    return re.match(pattern, filename) is not None

# Add more validation functions as needed, e.g., for passwords, user inputs etc.
'''
    return validators_utils