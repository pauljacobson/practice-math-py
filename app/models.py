# Import db from the app package to use a single shared instance
from app import db

# Import UserMixin from flask-login to add default implementations
# of is_authenticated, is_active, is_anonymous, and get_id
from flask_login import UserMixin

# Import password hashing utilities from werkzeug
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """User model with secure password hashing and Flask-Login integration."""

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Username must be unique and non-nullable
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Password hash — 256 chars to accommodate modern hash algorithms
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User %r>" % self.username
