# Import the SQLAlchemy class from the flask_sqlalchemy module
from flask_sqlalchemy import SQLAlchemy

# Import the generate_password_hash and check_password_hash functions
# from the werkzeug.security module
from werkzeug.security import generate_password_hash, check_password_hash

# Create an instance of the SQLAlchemy class
# This instance will be used to interact with the database
db = SQLAlchemy()


# Define a User model
class User(db.Model):
    # The id field is a primary key, which means that its values are unique and non-nullable
    id = db.Column(db.Integer, primary_key=True)

    # The username field is unique and non-nullable
    username = db.Column(db.String(80), unique=True, nullable=False)

    # The password_hash field is non-nullable
    password_hash = db.Column(db.String(120), nullable=False)

    # This method is used to set the password hash for a user
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # This method is used to check if the provided password matches the stored password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # This method returns a string representation of the User object
    def __repr__(self):
        return "<User %r>" % self.username
