from flask import Flask

# Factory function that creates and configures the Flask application instance
def create_app():
    app = Flask(__name__)
    
    # Secret key used for session data (like flash messages or login session)
    ## Note: Would in production be a secure key.
    app.config['SECRET_KEY'] = 'dev' 

    # SQLite database file path
    app.config['DATABASE'] = 'blog.db'  

    # Register routes (blueprint with all the app's routes)
    from . import routes
    app.register_blueprint(routes.bp)

    # Register database utilities (get_db, close_db, init_db, and so on)
    from . import db
    db.init_app(app)

    # Return the fully configured app
    return app
