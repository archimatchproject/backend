"""
utility function for users app
"""

from itsdangerous import BadSignature
from itsdangerous import SignatureExpired
from itsdangerous import URLSafeTimedSerializer

from project_core.django import base as settings


def generate_password_reset_token(user_id, expires_in=60):
    """
    Generate a password reset token for a user with a specified expiration time.

    Args:
        user_id (int): The ID of the user for whom the token is being generated.
        expires_in (int): The token expiration time in seconds.

    Returns:
        str: The generated password reset token.
    """
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY, expires_in)
    return serializer.dumps({"user_id": user_id}, salt="azaerzaratzaezae")


def validate_password_reset_token(token, max_age=60):
    """
    Validate a password reset token to ensure it is valid and has not expired.

    Args:
        token (str): The password reset token to validate.
        max_age (int): The maximum age of the token in seconds.

    Returns:
        tuple: A tuple containing the user ID (if valid) and an error message (if invalid).
    """
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        data = serializer.loads(token, salt="azaerzaratzaezae", max_age=max_age)
    except SignatureExpired:
        return None, "Token has expired"
    except BadSignature:
        return None, "Invalid token"
    return data["user_id"], None
