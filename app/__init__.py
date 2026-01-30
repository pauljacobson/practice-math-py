import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager

# Create shared extension instances at module level so other modules
# can import them (e.g. `from app import db, socketio`)
db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()

# Tell Flask-Login which endpoint handles unauthenticated users
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)

    # Core config from environment
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    # Build a default SQLite path using an absolute path so it resolves
    # consistently regardless of CWD (important for the debug reloader)
    basedir = os.path.abspath(os.path.dirname(__file__))
    default_db = "sqlite:///" + os.path.join(basedir, "app.db")

    # Handle the postgres:// -> postgresql:// rename that SQLAlchemy 1.4+ requires
    db_url = os.getenv("DATABASE_URL", default_db)
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    # Initialize extensions with this app
    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints after app is created to avoid
    # circular imports (models.py imports db from this module)
    from app.routes import bp as main_bp
    from app.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Create database tables if they don't exist yet
    with app.app_context():
        from app import models  # noqa: F401 — ensures models are registered
        db.create_all()

    return app
