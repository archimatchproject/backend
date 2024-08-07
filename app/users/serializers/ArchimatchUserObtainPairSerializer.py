"""
Module containing ArchimatchUserObtainPairSerializer class.

This module provides a custom serializer for obtaining JWT tokens,
enhanced with additional user information.

Classes:
    ArchimatchUserObtainPairSerializer: Serializer for obtaining JWT tokens with user data.
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.users import USER_TYPE_CHOICES
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.Client import Client
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


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

        super().validate(attrs)
        if self.user.is_deleted:
            raise serializers.ValidationError(detail="User has been deleted")
        refresh = self.get_token(self.user)
        access = refresh.access_token

        user_data = ArchimatchUserSerializer(self.user).data
        response_data = {
            "refresh": str(refresh),
            "access": str(access),
            "user": user_data,
        }
        if self.user.user_type == USER_TYPE_CHOICES[1][0]:
            is_verified = Client.objects.get(user=self.user).is_verified
            if is_verified:
                response_data["is_verified"] = is_verified
            else:
                response_data = {"is_verified": is_verified}

        return response_data


class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for obtaining JWT tokens with user data using phone_number field.

    This serializer extends TokenObtainPairSerializer to include user
    data in the token response.
    """

    username_field = "phone_number"
    phone_number = serializers.CharField()

    def validate(self, attrs):
        """
        Validate the data and return the custom response.

        Args:
            attrs: The attributes to validate.

        Returns:
            dict: Custom response containing the auth pair and user data.
        """

        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        user = ArchimatchUser.objects.filter(phone_number=phone_number).first()
        if self.user.is_deleted:
            raise serializers.ValidationError(detail="User has been deleted")
        if user and user.check_password(password):
            attrs["email"] = user.email
            attrs.pop("phone_number")
            self.username_field = "email"
            super().validate(attrs)

            refresh = self.get_token(self.user)
            access = refresh.access_token

            user_data = ArchimatchUserSerializer(self.user).data

            return {
                "refresh": str(refresh),
                "access": str(access),
                "user": user_data,
            }
        raise serializers.ValidationError("Invalid credentials")

    @classmethod
    def get_token(cls, user):
        """
        Return the token with additional user data serialized.

        Args:
            user: The user object for which the token is being obtained.

        Returns:
            RefreshToken: JWT refresh token.
        """
        token = super().get_token(user)
        return token
