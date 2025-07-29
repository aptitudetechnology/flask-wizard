"""
Wizard Prompts Module
Handles all user input gathering for the Flask App Generator.
"""

import sys

def gather_basic_info() -> dict:
    """Collect basic app information from the user."""
    print("\n📋 Basic Information")
    print("-" * 20)

    config = {}
    config['app_name'] = input("App name (lowercase, dashes ok): ").strip()
    if not config['app_name']:
        config['app_name'] = "my-flask-app"

    config['app_title'] = input("App display title: ").strip()
    if not config['app_title']:
        config['app_title'] = config['app_name'].replace('-', ' ').title()

    config['description'] = input("Brief description: ").strip()
    if not config['description']:
        config['description'] = f"A Flask web application: {config['app_title']}"

    config['author'] = input("Author name: ").strip()
    if not config['author']:
        config['author'] = "Developer"

    return config

def gather_nav_info() -> list:
    """Collect navigation structure from the user."""
    print("\n🧭 Navigation Setup")
    print("-" * 20)
    print("Enter dashboard navigation items (press Enter when done)")

    nav_items = []
    default_items = [
        {"name": "Dashboard", "route": "/", "icon": "home"},
        {"name": "Settings", "route": "/settings", "icon": "gear"}
    ]

    print("Default items: Dashboard, Settings")
    use_defaults = input("Use default navigation? (y/n): ").lower().startswith('y')

    if use_defaults:
        nav_items = default_items
    else:
        while True:
            item_name = input("Nav item name (or Enter to finish): ").strip()
            if not item_name:
                break

            route = input(f"Route for '{item_name}' (default: /{item_name.lower()}): ").strip()
            if not route:
                route = f"/{item_name.lower().replace(' ', '-')}"

            icon = input(f"Bootstrap icon name (default: circle): ").strip()
            if not icon:
                icon = "circle"

            nav_items.append({
                "name": item_name,
                "route": route,
                "icon": icon
            })

    return nav_items

def gather_features() -> dict:
    """Collect feature requirements from the user."""
    print("\n🔧 Features & Options")
    print("-" * 20)

    # Database
    print("Database options:")
    print("1. SQLite3 (default)")
    print("2. PostgreSQL ready (with SQLite fallback)")
    db_choice = input("Choose database (1/2): ").strip()
    database_choice = 'postgres_ready' if db_choice == '2' else 'sqlite'

    # Additional features
    features = {
        'user_auth': input("Include user authentication? (y/n): ").lower().startswith('y'),
        'file_uploads': input("Include file upload handling? (y/n): ").lower().startswith('y'),
        'api_endpoints': input("Include REST API endpoints? (y/n): ").lower().startswith('y'),
        'background_tasks': input("Include background task support? (y/n): ").lower().startswith('y'),
    }

    return {'database': database_choice, 'features': features}

def confirm_config(config: dict) -> bool:
    """Show configuration for confirmation to the user."""
    print("\n📝 Configuration Summary")
    print("-" * 30)
    print(f"App Name: {config['app_name']}")
    print(f"Title: {config['app_title']}")
    print(f"Author: {config['author']}")
    print(f"Database: {config['features']['database']}") # Access database from features dict
    print(f"Navigation items: {len(config['nav_items'])}")
    print(f"Features: {', '.join([k for k, v in config['features'].items() if k != 'database' and v])}")

    confirm = input("\nProceed with generation? (y/n): ").lower().startswith('y')
    return confirm