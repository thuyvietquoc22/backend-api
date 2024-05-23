from datetime import datetime

from jwt.exceptions import JWTDecodeError
from loguru import logger

from app.utils.jwt_service import JWTService


def test_create_jwt_token():
    payload = {
        "sub": 5650079079,
        "content": "test_content"
    }

    response = JWTService().generate_token(payload)
    # logger.info(f"Token: {response}")
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    assert len(response.split(".")) == 3  # JWT token has 3 parts separated by dot


def test_decode_jwt_token():
    payload = {
        "sub": "test",
        "content": "test_content"
    }
    token = JWTService().generate_token(payload)

    response = JWTService().decode_token(token)
    assert response is not None
    assert isinstance(response, dict)
    assert response.get("sub") == "test"
    assert response.get("content") == "test_content"


def test_decode_invalid_jwt_token():
    token = "invalid_token"
    try:
        response = JWTService().decode_token(token)
    except JWTDecodeError as e:
        assert str(e) == "failed to decode JWT"
        return
    assert False, "Token should be invalid"


def test_decode_token_expired():
    payload = {
        "sub": "test",
        "content": "test_content"
    }

    token = JWTService().generate_token(payload, time_expired=datetime.utcnow())

    try:
        JWTService().decode_token(token)
    except JWTDecodeError as e:
        assert str(e) == "JWT Expired"
        return
    assert False, "Token should be expired"


def test_decode_token_invalid_signature():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiY29udGVudCI6InRlc3RfY29udGVudCJ9.VB9fkBI28HXl1V0OFGWnBJbQeEbbh8FEaKgA2jqJwqg"
    try:
        response = JWTService().decode_token(token)
    except JWTDecodeError as e:
        assert str(e) == "failed to decode JWT"
        return
    assert False, "Token should have invalid signature"
