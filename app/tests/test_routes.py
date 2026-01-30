"""Tests for the main routes blueprint."""

from app.routes import allowed_file


def test_allowed_file_accepts_valid_extensions():
    """allowed_file should accept png, jpg, jpeg."""
    assert allowed_file("photo.png") is True
    assert allowed_file("photo.jpg") is True
    assert allowed_file("photo.jpeg") is True


def test_allowed_file_rejects_invalid_extensions():
    """allowed_file should reject non-image file types."""
    assert allowed_file("doc.txt") is False
    assert allowed_file("script.py") is False
    assert allowed_file("page.html") is False


def test_allowed_file_rejects_no_extension():
    """allowed_file should reject filenames without an extension."""
    assert allowed_file("noext") is False


def test_index_is_public(client):
    """GET / should be accessible without login."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Practice Math" in response.data


def test_chat_requires_login(client):
    """GET /chat should redirect to login when not authenticated."""
    response = client.get("/chat", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_clear_history_requires_login(client):
    """POST /clear-history should redirect to login when not authenticated."""
    response = client.post("/clear-history", follow_redirects=False)
    assert response.status_code == 302


def test_upload_requires_login(client):
    """POST /upload should redirect to login when not authenticated."""
    response = client.post("/upload", follow_redirects=False)
    assert response.status_code == 302
