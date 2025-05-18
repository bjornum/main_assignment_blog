from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'  # Needed for forms
    app.config['DATABASE'] = 'sqlite:///blog.db'

    from . import routes
    app.register_blueprint(routes.bp)

    return app
