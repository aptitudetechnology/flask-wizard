"""
Static Files Generator Module
Generates custom.css and app.js.
"""

def generate_custom_css_content(config: dict) -> str:
    """Generate custom.css file content."""
    app_title = config['app_title']
    custom_css = '''/* Custom styles for ''' + app_title + ''' */
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --success-color: #198754;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
}

body {
    background-color: #f8f9fa;
    display: flex;
    flex-direction: column;
    min-height: 100vh; /* Ensure footer sticks to bottom */
}

.navbar-brand {
    font-weight: bold;
}

.card {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    border: 1px solid rgba(0, 0, 0, 0.125);
    transition: box-shadow 0.15s ease-in-out;
}

.card:hover {
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.nav-link.active {
    font-weight: bold;
}

main {
    flex-grow: 1; /* Allow main content to take available space */
}

footer {
    margin-top: auto;
}

/* Utility classes */
.cursor-pointer {
    cursor: pointer;
}

.text-truncate-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Toast notifications */
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1050; /* Above modals */
}
'''
    return custom_css

def generate_app_js_content(config: dict) -> str:
    """Generate app.js file content."""
    app_title = config['app_title']
    app_js = '''// ''' + app_title + ''' JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log("''' + app_title + ''' loaded successfully");

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Loading...';
            }
        });
    });
});

// Utility functions
function showToast(message, type = 'info') {
    // Create a simple toast notification
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        // Create container if it doesn't exist
        const newToastContainer = document.createElement('div');
        newToastContainer.className = 'toast-container';
        document.body.appendChild(newToastContainer);
        toastContainer = newToastContainer;
    }

    const toastElement = document.createElement('div');
    toastElement.className = `alert alert-${type} alert-dismissible fade show`;
    toastElement.setAttribute('role', 'alert');
    toastElement.innerHTML = `
        <div>${message}</div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    toastContainer.appendChild(toastElement);

    // Auto-hide after 3 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(toastElement);
        bsAlert.close();
    }, 3000);
}
'''
    return app_js