# =========================================
# Application Entry Point (run.py)
# =========================================

# Import the Flask app factory function
from app import create_app

# Create the Flask app instance using the factory pattern
app = create_app()

# If this script is run directly (not imported), start the Flask development server
# Shows errors in the browser as debugging is enabled
if __name__ == "__main__":
    app.run(debug=True)
