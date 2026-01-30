"""Shared test fixtures for the Practice Math app.

Uses an in-memory SQLite database so tests run fast and don't
touch the real database.
"""

import pytest

from app import create_app, db as _db


@pytest.fixture()
def app():
    """Create an application instance configured for testing."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "test-secret-key",
            # Disable CSRF for simpler form testing
            "WTF_CSRF_ENABLED": False,
        }
    )

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture()
def client(app):
    """A Flask test client for making HTTP requests."""
    return app.test_client()


@pytest.fixture()
def db(app):
    """Provide the database session for direct model manipulation."""
    return _db
