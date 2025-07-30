#!/usr/bin/env python3
"""
Flask App Generator Wizard - Main Orchestrator
This script guides the user through creating a new Flask application,
gathering configuration, and then generating the project files.
"""

print("DEBUG: Script started.") 

import sys
import json
from pathlib import Path
from datetime import datetime

# Import modules for different wizard stages
from wizard_prompts import gather_basic_info, gather_nav_info, gather_features, confirm_config
from file_operations import create_directory_structure, write_file

# Import functions from app_generator package
from app_generator.core import generate_main_app_content, generate_paths_file_content
from app_generator.routes import generate_routes_init_content, generate_main_routes_content, generate_api_routes_content
from app_generator.templates import generate_base_template_content, generate_dashboard_template_content, generate_nav_templates_content, generate_error_template_content
from app_generator.utils import generate_utils_init_content, generate_database_utils_content, generate_helpers_utils_content, generate_validators_utils_content
from app_generator.static import generate_custom_css_content, generate_app_js_content
from app_generator.misc import generate_requirements_content, generate_readme_content, generate_env_content, generate_settings_content  



print("DEBUG: All imports complete.")

class FlaskWizard:
    def __init__(self):
        self.config = {}
        self.app_output_path = None
        print("DEBUG: FlaskWizard instance initialized.")

    def run(self):
        """Main wizard flow for generating a Flask application."""
        print("DEBUG: Entering FlaskWizard.run() method.")
        print("🧙‍♂️ Flask App Generator Wizard")
        print("=" * 40)

        # 1. Gather User Information
        self.config.update(gather_basic_info())
        self.config['nav_items'] = gather_nav_info()
        
        # --- START OF ROBUST FEATURES PROCESSING BLOCK (YOUR SUGGESTION) ---
        features_data_from_prompts = gather_features() or {} # Ensures it's always a dictionary
        
        # Safely get the 'features' dictionary, defaulting to an empty dict if not found
        features_dict = features_data_from_prompts.get('features', {})
        
        self.config['features'] = {
            # Safely get 'database', defaulting to 'sqlite'
            'database': features_data_from_prompts.get('database', 'sqlite'),
            # Safely get each feature's boolean value, defaulting to False if not found
            'user_auth': features_dict.get('user_auth', False),
            'file_uploads': features_dict.get('file_uploads', False),
            'api_endpoints': features_dict.get('api_endpoints', False),
            'background_tasks': features_dict.get('background_tasks', False)
        }
        # --- END OF ROBUST FEATURES PROCESSING BLOCK ---

        # 2. Confirm Configuration
        if not confirm_config(self.config):
            print("\nAborted by user. No files were generated.")
            sys.exit(0)

        # 3. Generate the Application
        print(f"\nGenerating Flask app '{self.config['app_name']}'...")
        self.generate_app()

        print(f"\n✅ Flask app '{self.config['app_name']}' created successfully!")
        print(f"📁 Location: {self.app_output_path.resolve()}")
        print(f"🚀 To run: cd {self.config['app_name']} && python app.py")
        print("\nDon't forget to create and activate a virtual environment!")
        print("Example: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt")


    def generate_app(self):
        """Generates the complete Flask application structure and files based on configuration."""
        print("DEBUG: Entering generate_app().")
        self.app_output_path = Path(self.config['app_name'])
        create_directory_structure(self.app_output_path)

        # Generate core application files
        write_file(self.app_output_path / "paths.py", generate_paths_file_content(self.config))
        write_file(self.app_output_path / "app.py", generate_main_app_content(self.config))
        write_file(self.app_output_path / ".env", generate_env_content(self.config))
        write_file(self.app_output_path / "requirements.txt", generate_requirements_content(self.config))
        write_file(self.app_output_path / "README.md", generate_readme_content(self.config))
        write_file(self.app_output_path / "settings.py", generate_settings_content(self.config))

        # Generate Route files
        write_file(self.app_output_path / "routes" / "__init__.py", generate_routes_init_content())
        write_file(self.app_output_path / "routes" / "main.py", generate_main_routes_content(self.config))
        # API routes are optional, generate only if API endpoints feature is selected
        if self.config['features']['api_endpoints']:
            write_file(self.app_output_path / "routes" / "api.py", generate_api_routes_content(self.config))
        else:
            # If API is not chosen, ensure api.py is minimal or not generated
            write_file(self.app_output_path / "routes" / "api.py", "# API routes (feature not enabled)\nfrom flask import Blueprint\napi_bp = Blueprint('api', __name__, url_prefix='/api')\n")


        # Generate Utility files
        write_file(self.app_output_path / "utils" / "__init__.py", generate_utils_init_content())
        write_file(self.app_output_path / "utils" / "database.py", generate_database_utils_content(self.config))
        write_file(self.app_output_path / "utils" / "helpers.py", generate_helpers_utils_content())
        write_file(self.app_output_path / "utils" / "validators.py", generate_validators_utils_content())

        # Generate Template files
        write_file(self.app_output_path / "templates" / "base.html", generate_base_template_content(self.config))
        write_file(self.app_output_path / "templates" / "dashboard.html", generate_dashboard_template_content(self.config))
        write_file(self.app_output_path / "templates" / "error.html", generate_error_template_content())
        # This function handles creating multiple navigation-related template files
        generate_nav_templates_content(self.app_output_path, self.config['nav_items'])

        # Generate Static files
        write_file(self.app_output_path / "static" / "css" / "custom.css", generate_custom_css_content(self.config))
        write_file(self.app_output_path / "static" / "js" / "app.js", generate_app_js_content(self.config))
        # Add this line with your other core application files
        write_file(self.app_output_path / "settings.py", generate_settings_content(self.config))


if __name__ == '__main__':
    print("DEBUG: Entering __name__ == '__main__' block.")
    wizard = FlaskWizard()
    try:
        wizard.run()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please check the traceback for more details.")
        sys.exit(1)