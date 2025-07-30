# flask-app-wizard

## Overview

The Flask App Generator Wizard is a Python-based command-line tool designed to quickly scaffold new Flask web applications. It guides you through a series of interactive prompts to gather your desired application name, features (like user authentication, API endpoints, database type), and navigation structure. Once configured, it generates a complete, modular Flask project ready for development.

This wizard aims to reduce boilerplate setup and provide a consistent, best-practice starting point for Flask projects.

## Features

- **Interactive Prompts**: User-friendly questions to customize your app.
- **Modular Design**: Generates a Flask app with a clear, organized directory structure using Blueprints, separating concerns for routes, templates, static files, and utilities.
- **Configurable Database**: Choose between SQLite3 for simple, file-based projects or a PostgreSQL-ready setup with SQLAlchemy for more robust, scalable applications.
- **Common Features**: Options to include basic user authentication, file upload handling, REST API endpoints, and background task support.
- **Bootstrap 5 Integration**: Generated templates come with Bootstrap 5 and Bootstrap Icons for a modern, responsive UI.
- **Environment Variable Support**: Uses `.env` files for easy configuration management.
- **Logging**: Basic application logging configured out-of-the-box.

## Getting Started

Follow these steps to set up and run the Flask App Generator Wizard.

### 1. Clone the Repository

First, clone this wizard's repository to your local machine:

```bash
git clone https://github.com/aptitudetechnology/flask-wizard
cd flask-app-wizard
```

### 2. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage the wizard's dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the necessary Python packages for the wizard to run:

```bash
pip install -r requirements.txt
```

### 4. Run the Wizard

Execute the main wizard script:

```bash
python main_wizard.py
```

### 5. Follow the Prompts

The wizard will ask you a series of questions:

- **Basic Information**: App name, display title, description, and author.
- **Navigation Setup**: Define the main navigation items for your dashboard.
- **Features & Options**: Select your preferred database and optional features like user authentication, file uploads, API endpoints, and background tasks.

After you confirm your choices, the wizard will generate your new Flask application in a directory named after your chosen app name.

## Example Usage

Here's an example of how you might interact with the wizard when running `python main_wizard.py`:

```text
Welcome to the Flask App Generator Wizard!

App Name: my_flask_app
Display Title: My Flask App
Description: A sample Flask application
Author: Jane Doe

Select database (1) SQLite3 (2) PostgreSQL: 1
Include user authentication? (y/n): y
Include file uploads? (y/n): n
Include REST API endpoints? (y/n): y
Include background task support? (y/n): n

Generating project files...
Success! Your Flask app is ready in ./my_flask_app
```

## Project Structure (Wizard Itself)

```
flask-app-wizard/
├── templates/          # Jinja2 templates used for generating Flask app structure
├── static/             # Static assets for generated apps (CSS/JS/Icons)
├── wizard/             # Core logic of the app generator
│   ├── prompts.py      # Interactive CLI logic
│   ├── generator.py    # File and directory generator
│   └── utils.py        # Utility functions
├── main_wizard.py      # Entry point for the CLI wizard
├── requirements.txt    # Python package dependencies
└── README.md           # Project overview and usage instructions
```

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please feel free to:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a Pull Request.

## License

This project is open-source and available under the [AGPL License](LICENSE).
