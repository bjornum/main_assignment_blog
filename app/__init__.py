from flask import Flask

def create_app():
    app = Flask(__name__)
    # Needed for forms
    app.config['SECRET_KEY'] = 'dev'  
    # No sqlite:/// needed here
    app.config['DATABASE'] = 'blog.db'  

    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)

    # Register database
    from . import db
    db.init_app(app)

    return app
