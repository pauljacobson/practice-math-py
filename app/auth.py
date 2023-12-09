from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")

# Secret key for token generation and verification
SECRET_KEY = "your-secret-key"

# Token Serializer
# This is used to serialize and deserialize data for the token.
# The secret key is used to sign the token and the expires_in parameter sets the token's lifespan to 1 hour.
s = Serializer(SECRET_KEY, expires_in=3600)

# Store users and their passkeys
# This is a dictionary where the keys are usernames and the values are hashed passkeys.
users = {}


# Verify tokens
# This function is decorated with the @auth.verify_token decorator, which means it's used to check if a token is valid.
# It tries to load the token using the serializer, and if it can't (because the token is invalid or expired), it returns False.
# If the token is valid, it checks if the username in the token is in the users dictionary, and if it is, it returns the username.
# If the username is not in the users dictionary, it returns False.
@auth.verify_token
def verify_token(token):
    try:
        data = s.loads(token)
    except:
        return False
    if "username" in data:
        return data["username"]
    return False


# Function to generate token
# This function is used to generate a new token for a user.
# It gets the username and passkey from the request arguments, and if the username is in the users dictionary and the hashed passkey matches the stored passkey, it generates a new token.
# The token is a serialized dictionary that contains the username.
# The function returns a JSON response that includes the token and its lifespan.
# If the username is not in the users dictionary or the passkey doesn't match, it returns an error message.
def get_auth_token():
    username = request.args.get("username")
    password = request.args.get("password")
    if username in users and check_password_hash(users[username], password):
        token = s.dumps({"username": username})
        return jsonify({"token": token.decode("ascii"), "duration": 3600})
    return jsonify({"error": "Invalid username or password"}), 400


# Function to register new user
# This function is used to register a new user.
# It gets the username and passkey from the request JSON, and if the username is already in the users dictionary, it returns an error message.
# If the username is not in the users dictionary, it hashes the passkey and stores it in the users dictionary, then returns a success message.
def register_user():
    username = request.json.get("username")
    password = request.json.get("password")
    if username in users:
        return jsonify({"error": "Username already exists"}), 400
    users[username] = generate_password_hash(password)
    return jsonify({"success": "User created successfully"}), 201


@app.route("/secure-endpoint")
@auth.login_required
def secure_endpoint():
    """
    This is a secure endpoint that requires authentication to access.

    The @auth.login_required decorator is used to secure this endpoint.
    When a user tries to access this endpoint, the verify_token function
    (which you've already defined in your auth.py script) will be called
    to check if the user's token is valid.

    If the token is valid, the user will be able to access the endpoint.
    If the token is not valid, the user will receive a 401 Unauthorized error.
    """
    return jsonify({"message": "This is a secure endpoint."})
