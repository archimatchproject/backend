"""
Module containing ArchimatchUserObtainPairSerializer class.

This module provides a custom serializer for obtaining JWT tokens,
enhanced with additional user information.

Classes:
    ArchimatchUserObtainPairSerializer: Serializer for obtaining JWT tokens with user data.
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from app.users.serializers import ArchimatchUserSerializer


class ArchimatchUserObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for obtaining JWT tokens with user data.

    This serializer extends TokenObtainPairSerializer to include user
    data in the token response.
    """

    @classmethod
    def get_token(cls, user):
        """
        Return the token with additional user data serialized.

        Args:
            user: The user object for which the token is being obtained.

        Returns:
            RefreshToken: JWT refresh token.
        """
        return super().get_token(user)

    def validate(self, attrs):
        """
        Validate the data and return the custom response.

        Args:
            attrs: The attributes to validate.

        Returns:
            dict: Custom response containing the auth pair and user data.
        """
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        access = refresh.access_token

        user_data = ArchimatchUserSerializer(self.user).data

        return {
            "refresh": str(refresh),
            "access": str(access),
            "user": user_data,
        }
