import pytest
from unittest.mock import Mock
from your_flask_app.auth import verify_token, s, User


def test_verify_token(mocker):
    # Mock the loads method of the Serializer
    mocker.patch.object(s, "loads", return_value={"username": "testuser"})

    # Mock the User.query.filter_by method
    mock_filter_by = mocker.patch("your_flask_app.auth.User.query.filter_by")
    mock_user = Mock()
    mock_user.username = "testuser"
    mock_filter_by.return_value.first.return_value = mock_user

    result = verify_token("testtoken")
    assert result.username == "testuser"
