import pytest
from unittest.mock import Mock
from your_flask_app.auth import verify_token, s, User


def test_ask_openai(mocker):
    # Mock the OpenAI API
    mocker.patch(
        "openai.ChatCompletion.create",
        return_value={"choices": [{"message": {"content": "Answer"}}]},
    )

    result = ask_openai("Question")
    assert result == "Answer"
