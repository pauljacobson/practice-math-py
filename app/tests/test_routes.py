import pytest
from unittest.mock import Mock
from your_flask_app.auth import verify_token, s, User


def test_allowed_file():
    assert allowed_file("test.png") == True
    assert allowed_file("test.txt") == False


def test_handle_message(mocker):
    # Mock the ask_openai function
    mocker.patch("app.routes.ask_openai", return_value="Answer")

    # Mock the socketio.emit function
    mock_emit = mocker.patch("flask_socketio.SocketIO.emit")

    handle_message({"text": "Question"})
    mock_emit.assert_called_once_with("response", {"text": "Answer"})
