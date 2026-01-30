"""Tests for the Anthropic Claude integration module."""

from unittest.mock import MagicMock, patch

from app.claude_integration import ask_claude


def test_ask_claude_returns_response(app):
    """ask_claude should return the text from Claude's response."""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="The answer is 42.")]

    with app.test_request_context():
        with patch("app.claude_integration.client") as mock_client:
            mock_client.messages.create.return_value = mock_response
            result = ask_claude("What is 6 times 7?")

    assert result == "The answer is 42."


def test_ask_claude_stores_history(app):
    """ask_claude should store conversation history in the session."""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Hello!")]

    with app.test_request_context():
        from flask import session

        with patch("app.claude_integration.client") as mock_client:
            mock_client.messages.create.return_value = mock_response
            ask_claude("Hi")

        assert len(session["conversation_history"]) == 2
        assert session["conversation_history"][0] == {"role": "user", "content": "Hi"}
        assert session["conversation_history"][1] == {"role": "assistant", "content": "Hello!"}


def test_ask_claude_handles_auth_error(app):
    """ask_claude should return a user-friendly message on auth failure."""
    import anthropic

    with app.test_request_context():
        with patch("app.claude_integration.client") as mock_client:
            mock_client.messages.create.side_effect = anthropic.AuthenticationError(
                message="invalid key",
                response=MagicMock(status_code=401),
                body={"error": {"message": "invalid key"}},
            )
            result = ask_claude("test")

    assert "authentication error" in result.lower()


def test_ask_claude_handles_rate_limit(app):
    """ask_claude should return a user-friendly message on rate limit."""
    import anthropic

    with app.test_request_context():
        with patch("app.claude_integration.client") as mock_client:
            mock_client.messages.create.side_effect = anthropic.RateLimitError(
                message="rate limited",
                response=MagicMock(status_code=429),
                body={"error": {"message": "rate limited"}},
            )
            result = ask_claude("test")

    assert "try again" in result.lower()
