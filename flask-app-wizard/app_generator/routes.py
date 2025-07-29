"""
Routes Generator Module
Generates the __init__.py, main.py, and api.py for Flask blueprints.
"""

def generate_routes_init_content() -> str:
    """Generate __init__.py file content for the routes package."""
    routes_init = '''"""
Routes package for organized route handling
"""

from .main import main_bp
from .api import api_bp

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
'''
    return routes_init

def generate_blueprint_route_handlers(nav_items: list) -> str:
    """Helper to generate route handlers for navigation items as blueprint methods."""
    routes = []

    for item in nav_items:
        # Dashboard and Settings are often handled explicitly in main.py, or
        # default to a simpler render_template if not special.
        # This function generates content for *additional* nav items.
        if item['route'] == '/' or item['name'].lower() == 'settings':
            continue

        route_name = item['name'].lower().replace(' ', '_')
        routes.append(f'''
@main_bp.route('{item['route']}')
def {route_name}():
    """{item['name']} page"""
    # Example: log_user_action('view_{route_name}', request.remote_addr)
    return render_template('{route_name}.html', title='{item['name']}')
''')
    return '\n'.join(routes)

def generate_main_routes_content(config: dict) -> str:
    """Generate main.py file content for core application routes."""
    app_title = config['app_title']
    # Use helper function to generate additional routes
    additional_routes = generate_blueprint_route_handlers(config['nav_items'])

    main_routes = f'''"""
Main application routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from utils.database import get_db_connection
from utils.helpers import log_user_action
import logging

logger = logging.getLogger(__name__)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    """Main dashboard"""
    log_user_action('dashboard_visit', request.remote_addr)
    return render_template('dashboard.html', title='Dashboard')

{additional_routes}

@main_bp.route('/settings')
def settings():
    """Application settings"""
    return render_template('settings.html', title='Settings')

# Example: A simple form route
@main_bp.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        feedback_text = request.form.get('feedback_text')
        if feedback_text:
            # In a real app, you'd save this to a database
            logger.info(f"Received feedback: {{feedback_text}} from {{request.remote_addr}}")
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Feedback cannot be empty.', 'error')
    return render_template('feedback.html', title='Submit Feedback')
'''
    return main_routes

def generate_api_routes_content(config: dict) -> str:
    """Generate api.py file content for REST API endpoints."""
    app_title = config['app_title']
    include_api_data_endpoint = config['features']['api_endpoints']

    api_routes = '''"""
API routes for REST endpoints
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
from utils.database import get_db_connection, get_setting # get_setting for potential API key validation
from utils.helpers import validate_api_key # Assuming you'd add this utility
import logging

logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__)

@api_bp.route('/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": get_setting('version', 'N/A'),
        "service": "''' + app_title + '''"
    })

@api_bp.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        conn = get_db_connection()
        conn.execute('SELECT 1')
        conn.close()

        return jsonify({
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"API Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

''' + ('''@api_bp.route('/data')
def get_data():
    """Get application data (example protected endpoint)"""
    # Example API endpoint - customize as needed
    # if not validate_api_key(request.headers.get('X-API-Key')):
    #     return jsonify({"error": "Unauthorized"}), 401

    try:
        conn = get_db_connection()
        # Fetch some example data; adjust query as per your app's needs
        cursor = conn.execute('SELECT key, value FROM app_settings LIMIT 10')
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({
            "success": True,
            "data": data,
            "count": len(data)
        })
    except Exception as e:
        logger.error(f"API data fetch failed: {e}")
        return jsonify({
            "success": False,
            "error": "Data fetch failed"
        }), 500
''' if include_api_data_endpoint else '')

    return api_routes