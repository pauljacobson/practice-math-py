"""Tests for the authentication blueprint (login, logout, register)."""

from app.models import User


def test_login_page_renders(client):
    """GET /login should return the login form."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_register_page_renders(client):
    """GET /register should return the registration form."""
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data


def test_register_creates_user(client, db):
    """POST /register should create a new user and redirect to login."""
    response = client.post(
        "/register",
        data={"username": "testuser", "password": "testpass"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

    user = User.query.filter_by(username="testuser").first()
    assert user is not None
    assert user.check_password("testpass")


def test_register_duplicate_username(client, db):
    """Registering with an existing username should redirect back with error."""
    # Create initial user
    client.post("/register", data={"username": "dup", "password": "pass"})
    # Try to register again with same username
    response = client.post(
        "/register",
        data={"username": "dup", "password": "pass2"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/register" in response.headers["Location"]


def test_login_valid_credentials(client, db):
    """Logging in with valid credentials should redirect to chat."""
    client.post("/register", data={"username": "user1", "password": "pass1"})
    response = client.post(
        "/login",
        data={"username": "user1", "password": "pass1"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/chat" in response.headers["Location"]


def test_login_invalid_credentials(client, db):
    """Logging in with wrong password should redirect back to login."""
    client.post("/register", data={"username": "user2", "password": "pass2"})
    response = client.post(
        "/login",
        data={"username": "user2", "password": "wrongpass"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_logout(client, db):
    """POST /logout should log the user out and redirect to index."""
    client.post("/register", data={"username": "user3", "password": "pass3"})
    client.post("/login", data={"username": "user3", "password": "pass3"})
    response = client.post("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert "/" in response.headers["Location"]


def test_chat_requires_login(client):
    """GET /chat without logging in should redirect to login."""
    response = client.get("/chat", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
