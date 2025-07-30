#!/usr/bin/env python3
"""
Flask App Generator Wizard - Main Orchestrator
This script guides the user through creating a new Flask application,
gathering configuration, and then generating the project files.
"""

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
from app_generator.misc import generate_requirements_content, generate_readme_content, generate_env_content

class FlaskWizard:
    def __init__(self):
        self.config = {}
        self.app_output_path = None # This will be the path to the newly generated Flask app

    def run(self):
        """Main wizard flow"""
        print("🧙‍♂️ Flask App Generator Wizard")
        print("=" * 40)

        # 1. Gather User Information
        self.config.update(gather_basic_info())
        self.config['nav_items'] = gather_nav_info()
        features_data = gather_features()
        
        # Flatten the features structure for compatibility with generators
        self.config['features'] = {
            'database': features_data['database'],
            'user_auth': features_data['features']['user_auth'],
            'file_uploads': features_data['features']['file_uploads'],
            'api_endpoints': features_data['features']['api_endpoints'],
            'background_tasks': features_data['features']['background_tasks']
        }

        # 2. Confirm Configuration
        if not confirm_config(self.config):
            print("Aborted by user.")
            sys.exit(0)

        # 3. Generate the Application
        self.generate_app()

        print(f"\n✅ Flask app '{self.config['app_name']}' created successfully!")
        print(f"📁 Location: {self.app_output_path}")
        print(f"🚀 To run: cd {self.config['app_name']} && python app.py")

    def generate_app(self):
        """Generate the complete Flask application structure and files."""
        self.app_output_path = Path(self.config['app_name'])
        create_directory_structure(self.app_output_path)

        # Generate files using content from app_generator modules
        write_file(self.app_output_path / "paths.py", generate_paths_file_content(self.config))
        write_file(self.app_output_path / "app.py", generate_main_app_content(self.config))
        write_file(self.app_output_path / ".env", generate_env_content(self.config))
        write_file(self.app_output_path / "requirements.txt", generate_requirements_content(self.config))
        write_file(self.app_output_path / "README.md", generate_readme_content(self.config))

        # Routes
        write_file(self.app_output_path / "routes" / "__init__.py", generate_routes_init_content())
        write_file(self.app_output_path / "routes" / "main.py", generate_main_routes_content(self.config))
        write_file(self.app_output_path / "routes" / "api.py", generate_api_routes_content(self.config))

        # Utils
        write_file(self.app_output_path / "utils" / "__init__.py", generate_utils_init_content())
        write_file(self.app_output_path / "utils" / "database.py", generate_database_utils_content(self.config))
        write_file(self.app_output_path / "utils" / "helpers.py", generate_helpers_utils_content())
        write_file(self.app_output_path / "utils" / "validators.py", generate_validators_utils_content())

        # Templates
        write_file(self.app_output_path / "templates" / "base.html", generate_base_template_content(self.config))
        write_file(self.app_output_path / "templates" / "dashboard.html", generate_dashboard_template_content(self.config))
        write_file(self.app_output_path / "templates" / "error.html", generate_error_template_content())
        generate_nav_templates_content(self.app_output_path, self.config['nav_items']) # This function handles multiple files

        # Static files
        write_file(self.app_output_path / "static" / "css" / "custom.css", generate_custom_css_content(self.config))
        write_file(self.app_output_path / "static" / "js" / "app.js", generate_app_js_content(self.config))


if __name__ == '__main__':
    wizard = FlaskWizard()
    wizard.run()