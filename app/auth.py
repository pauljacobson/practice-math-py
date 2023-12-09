import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_httpauth import HTTPTokenAuth
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User, db

load_dotenv()  # take environment variables from .env.
s = Serializer(os.getenv("SECRET_KEY"), expires_in=3600)

auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    user = User.query.filter_by(username=data["username"]).first()
    return user


@app.route("/token")
def get_auth_token():
    username = request.args.get("username")
    password = request.args.get("password")
    if username is None or password is None:
        return jsonify({"error": "Missing username or password"}), 400
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = s.dumps({"username": username})
        return jsonify({"token": token.decode("ascii"), "duration": 3600})
    return jsonify({"error": "Invalid username or password"}), 400


@app.route("/register", methods=["POST"])
def register_user():
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        return jsonify({"error": "Missing username or password"}), 400
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "Username already exists"}), 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"success": "User created successfully"}), 201

