"""
Wizard Prompts Module
Handles all user input gathering for the Flask App Generator using Questionary.
"""
import sys
import questionary
from questionary import Style


# Custom style for the wizard
wizard_style = Style([
    ('qmark', 'fg:#ff9d00 bold'),       # Question mark - orange
    ('question', 'bold'),                # Question text
    ('answer', 'fg:#ff9d00 bold'),       # User's answer - orange
    ('pointer', 'fg:#ff9d00 bold'),      # Pointer for selections - orange
    ('highlighted', 'fg:#ff9d00 bold'),  # Highlighted choice - orange
    ('selected', 'fg:#ff9d00'),          # Selected choice - orange
    ('separator', 'fg:#cc5454'),         # Separators - red
    ('instruction', ''),                 # Instructions
    ('text', ''),                        # Default text
    ('disabled', 'fg:#858585 italic')    # Disabled choices - gray
])


def gather_basic_info() -> dict:
    """Collect basic app information from the user."""
    print("\n📋 Basic Information")
    print("-" * 20)
    
    config = {}
    
    # App name with validation
    config['app_name'] = questionary.text(
        "App name (lowercase, dashes ok):",
        default="my-flask-app",
        validate=lambda text: len(text.strip()) > 0 or "App name cannot be empty",
        style=wizard_style
    ).ask()
    
    # App title
    default_title = config['app_name'].replace('-', ' ').title()
    config['app_title'] = questionary.text(
        "App display title:",
        default=default_title,
        style=wizard_style
    ).ask()
    
    # Description
    default_description = f"A Flask web application: {config['app_title']}"
    config['description'] = questionary.text(
        "Brief description:",
        default=default_description,
        style=wizard_style
    ).ask()
    
    # Author
    config['author'] = questionary.text(
        "Author name:",
        default="Developer",
        style=wizard_style
    ).ask()
    
    return config


def gather_nav_info() -> list:
    """Collect navigation structure from the user."""
    print("\n🧭 Navigation Setup")
    print("-" * 20)
    
    default_items = [
        {"name": "Dashboard", "route": "/", "icon": "home"},
        {"name": "Settings", "route": "/settings", "icon": "gear"}
    ]
    
    use_defaults = questionary.confirm(
        "Use default navigation (Dashboard, Settings)?",
        default=True,
        style=wizard_style
    ).ask()
    
    if use_defaults:
        return default_items
    
    nav_items = []
    print("\nEnter your navigation items:")
    
    while True:
        # Ask if they want to add another item
        if nav_items:  # If we already have items
            add_more = questionary.confirm(
                f"Add another navigation item? (currently have {len(nav_items)})",
                default=True,
                style=wizard_style
            ).ask()
            if not add_more:
                break
        
        # Get item name
        item_name = questionary.text(
            "Navigation item name:",
            validate=lambda text: len(text.strip()) > 0 or "Item name cannot be empty",
            style=wizard_style
        ).ask()
        
        # Generate default route from name
        default_route = f"/{item_name.lower().replace(' ', '-')}"
        route = questionary.text(
            f"Route for '{item_name}':",
            default=default_route,
            style=wizard_style
        ).ask()
        
        # Icon selection with common choices
        icon_choices = [
            "home", "gear", "person", "file-text", "graph-up", 
            "table", "calendar", "envelope", "search", "plus-circle",
            "circle"  # default fallback
        ]
        
        icon = questionary.select(
            f"Bootstrap icon for '{item_name}':",
            choices=icon_choices,
            default="circle",
            style=wizard_style
        ).ask()
        
        nav_items.append({
            "name": item_name,
            "route": route,
            "icon": icon
        })
        
        # Break if they have quite a few items
        if len(nav_items) >= 8:
            questionary.print("That's quite a few items! You can always add more later.", style="fg:#858585")
            break
    
    return nav_items


def gather_features() -> dict:
    """Collect feature requirements from the user."""
    print("\n🔧 Features & Options")
    print("-" * 20)
    
    # Database selection
    database_choice = questionary.select(
        "Choose your database:",
        choices=[
            questionary.Choice("SQLite3 (simple, file-based)", "sqlite"),
            questionary.Choice("PostgreSQL ready (with SQLite fallback)", "postgres_ready")
        ],
        default="sqlite",
        style=wizard_style
    ).ask()
    
    # Feature selection using checkboxes for multiple features
    selected_features = questionary.checkbox(
        "Select features to include:",
        choices=[
            questionary.Choice("User authentication", "user_auth"),
            questionary.Choice("File upload handling", "file_uploads"),
            questionary.Choice("REST API endpoints", "api_endpoints"),
            questionary.Choice("Background task support", "background_tasks")
        ],
        style=wizard_style
    ).ask()
    
    # Convert list to boolean dict
    features = {
        'user_auth': 'user_auth' in selected_features,
        'file_uploads': 'file_uploads' in selected_features,
        'api_endpoints': 'api_endpoints' in selected_features,
        'background_tasks': 'background_tasks' in selected_features,
    }
    
    return {'database': database_choice, 'features': features}


def confirm_config(config: dict) -> bool:
    """Show configuration for confirmation to the user."""
    print("\n📝 Configuration Summary")
    print("-" * 30)
    print(f"App Name: {config['app_name']}")
    print(f"Title: {config['app_title']}")
    print(f"Author: {config['author']}")
    
    print(f"Database: {config['features']['database']}")
    feature_keys = ['user_auth', 'file_uploads', 'api_endpoints', 'background_tasks']
    selected_features = [k.replace('_', ' ').title() for k in feature_keys if config['features'].get(k, False)]
    
    print(f"Navigation items: {len(config['nav_items'])}")
    
    if selected_features:
        print(f"Features: {', '.join(selected_features)}")
    else:
        print("Features: None selected")
    
    return questionary.confirm(
        "\nProceed with generation?",
        default=True,
        style=wizard_style
    ).ask()