"""Authentication blueprint using Flask-Login and server-side sessions.

Provides login, logout, and registration routes.  Replaces the previous
itsdangerous / flask-httpauth token-based system with session cookies
managed by Flask-Login.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required

from app import db, login_manager
from app.models import User

# Blueprint for auth-related routes
auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    """Callback used by Flask-Login to reload a user from the session."""
    return db.session.get(User, int(user_id))


# ---- Login ----

@auth_bp.route("/login", methods=["GET"])
def login():
    """Render the login form."""
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login_post():
    """Process login credentials submitted via form or JSON."""
    # Support both form submissions and JSON API calls
    if request.is_json:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

    if not username or not password:
        flash("Please enter both username and password.", "error")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        flash("Invalid username or password.", "error")
        return redirect(url_for("auth.login"))

    login_user(user)
    # Redirect to the page the user originally wanted, or chat by default
    next_page = request.args.get("next") or url_for("main.chat")
    return redirect(next_page)


# ---- Logout ----

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """Log out the current user and clear conversation history."""
    session.pop("conversation_history", None)
    logout_user()
    return redirect(url_for("main.index"))


# ---- Registration ----

@auth_bp.route("/register", methods=["GET"])
def register():
    """Render the registration form."""
    return render_template("register.html")


@auth_bp.route("/register", methods=["POST"])
def register_post():
    """Create a new user account."""
    if request.is_json:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

    if not username or not password:
        flash("Please enter both username and password.", "error")
        return redirect(url_for("auth.register"))

    if User.query.filter_by(username=username).first() is not None:
        flash("Username already exists.", "error")
        return redirect(url_for("auth.register"))

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    flash("Account created! Please log in.", "success")
    return redirect(url_for("auth.login"))
