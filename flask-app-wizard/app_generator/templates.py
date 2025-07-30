"""
Templates Generator Module
Generates base.html, dashboard.html, error.html, and other navigation templates.
"""

from pathlib import Path
from datetime import datetime

def generate_base_template_content(config: dict) -> str:
    """Generate the base.html template content."""
    app_title = config['app_title']
    
    # Build the template content without f-string conflicts
    base_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title + ' - ' + ''' + f"'{app_title}'" + ''' if title else ''' + f"'{app_title}'" + ''' }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/custom.css') }}" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('main.dashboard') }}">
                <i class="bi bi-app"></i> ''' + app_title + '''
            </a>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    {% for item in nav_items %}
                    <li class="nav-item">
                        <a class="nav-link {{ 'active' if request.endpoint == 'main.' + item.name.lower().replace(' ', '_') else '' }}"
                           href="{{ url_for('main.' + item.name.lower().replace(' ', '_')) }}">
                            <i class="bi bi-{{ item.icon }}"></i> {{ item.name }}
                        </a>
                    </li>
                    {% endfor %}
                </ul>
                <ul class="navbar-nav">
                    {# Add user-specific links here if authentication is enabled #}
                    {% if 'user_auth' in features and features.user_auth %}
                    {# Example: Login/Logout links #}
                    {# <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.login') }}">Login</a></li> #}
                    {# <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.logout') }}">Logout</a></li> #}
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    <footer class="bg-light mt-5 py-3">
        <div class="container text-center text-muted">
            <small>&copy; {{ current_year }} ''' + app_title + ''' | Built with Flask</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>'''
    return base_template

def generate_dashboard_template_content(config: dict) -> str:
    """Generate the dashboard.html template content."""
    app_title = config['app_title']
    description = config['description']
    
    dashboard_template = '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1>Welcome to ''' + app_title + '''</h1>
        <p class="lead">''' + description + '''</p>
    </div>
</div>

<div class="row mt-4">
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title"><i class="bi bi-info-circle"></i> Status</h5>
                <p class="card-text">System is running normally</p>
                <span class="badge bg-success">Online</span>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title"><i class="bi bi-clock"></i> Last Updated</h5>
                <p class="card-text">{{ format_datetime(datetime.now()) }}</p>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title"><i class="bi bi-gear"></i> Quick Actions</h5>
                <a href="{{ url_for('main.settings') }}" class="btn btn-outline-primary btn-sm">Settings</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    return dashboard_template

def generate_nav_templates_content(app_path: Path, nav_items: list):
    """Generate HTML templates for each custom navigation item."""
    for item in nav_items:
        if item['route'] == '/' or item['name'].lower() == 'settings':
            continue

        template_name = item['name'].lower().replace(' ', '_')
        page_template = '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1><i class="bi bi-''' + item['icon'] + '''"></i> ''' + item['name'] + '''</h1>
        <p>This is the ''' + item['name'].lower() + ''' page. Add your content here.</p>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">''' + item['name'] + ''' Content</h5>
                <p class="card-text">Customize this section for your ''' + item['name'].lower() + ''' functionality.</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

        (app_path / "templates" / f"{template_name}.html").write_text(page_template)
        print(f"Generated: {app_path / 'templates' / f'{template_name}.html'}")

def generate_error_template_content() -> str:
    """Generate the error.html template content."""
    error_template = '''{% extends "base.html" %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 text-center">
        <h1 class="display-1">{{ code }}</h1>
        <h2>{{ error }}</h2>
        <p class="lead">Sorry, something went wrong.</p>
        <a href="{{ url_for('main.dashboard') }}" class="btn btn-primary">Go Home</a>
    </div>
</div>
{% endblock %}'''
    return error_template