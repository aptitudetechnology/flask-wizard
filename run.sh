#!/bin/bash

# Define the base directory for the wizard project
WIZARD_DIR="flask-app-wizard"

# Define the app generator package directory
APP_GENERATOR_DIR="$WIZARD_DIR/app_generator"

echo "Creating modular directory structure for the Flask App Wizard..."

# Create the main wizard project directory
mkdir -p "$WIZARD_DIR"
echo "Created: $WIZARD_DIR/"

# Create top-level modules within the wizard directory
touch "$WIZARD_DIR/main_wizard.py"
touch "$WIZARD_DIR/wizard_prompts.py"
touch "$WIZARD_DIR/file_operations.py"
echo "Created: main_wizard.py, wizard_prompts.py, file_operations.py inside $WIZARD_DIR/"

# Create the app_generator package directory
mkdir -p "$APP_GENERATOR_DIR"
echo "Created: $APP_GENERATOR_DIR/"

# Create the __init__.py file for the app_generator package
touch "$APP_GENERATOR_DIR/__init__.py"
echo "Created: $APP_GENERATOR_DIR/__init__.py"

# Create sub-modules within the app_generator package
touch "$APP_GENERATOR_DIR/core.py"
touch "$APP_GENERATOR_DIR/routes.py"
touch "$APP_GENERATOR_DIR/templates.py"
touch "$APP_GENERATOR_DIR/utils.py"
touch "$APP_GENERATOR_DIR/static.py"
touch "$APP_GENERATOR_DIR/misc.py"
echo "Created core.py, routes.py, templates.py, utils.py, static.py, misc.py inside $APP_GENERATOR_DIR/"

echo ""
echo "Modular directory structure created successfully!"
echo "You can now populate these files with the refactored code."
echo "To get started, you might want to add basic shebangs and docstrings to the .py files."