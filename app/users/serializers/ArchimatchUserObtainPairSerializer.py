"""
Module containing ArchimatchUserObtainPairSerializer class.

This module provides a custom serializer for obtaining JWT tokens,
enhanced with additional user information.

Classes:
    ArchimatchUserObtainPairSerializer: Serializer for obtaining JWT tokens with user data.
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.users.serializers import ArchimatchUserSerializer


class ArchimatchUserObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for obtaining JWT tokens with user data.

    This serializer extends TokenObtainPairSerializer to include user
    data in the token response.

    Methods:
        get_token(cls, user):
            Returns the token with additional user data serialized.
    """

    @classmethod
    def get_token(cls, user):
        """
        Return the token with additional user data serialized.

        Args:
            user: The user object for which the token is being obtained.

        Returns:
            dict: JWT token with user data serialized.
        """
        token = super().get_token(user)
        token["user"] = ArchimatchUserSerializer(user).data
        return token
