from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .extensions import db, login_manager

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    from .routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app
