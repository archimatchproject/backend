"""
Module containing ArchimatchUserSerializer and ArchimatchUserSimpleSerializer classes.

This module provides serializers for the ArchimatchUser model, tailored for different use cases.

Classes:
    ArchimatchUserSerializer: Detailed serializer for ArchimatchUser model.
    ArchimatchUserSimpleSerializer: Simplified serializer for ArchimatchUser model.
"""

from rest_framework import serializers

from app.users.models import ArchimatchUser


class ArchimatchUserSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for ArchimatchUser model.

    This serializer includes all fields of the ArchimatchUser model for detailed serialization.

    Fields:
        username: Username of the user.
        first_name: First name of the user.
        last_name: Last name of the user.
        email: Email address of the user.
        phone_number: Phone number of the user.
        image: Image associated with the user.
        user_type: Type of the user.
    """

    class Meta:
        """
        Meta class for ArchimatchUserSerializer.

        Includes detailed fields for serialization and additional options.
        """

        model = ArchimatchUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "image",
            "user_type",
        ]
        extra_kwargs = {
            "username": {"read_only": True},
            "email": {"required": True},
        }


class ArchimatchUserSimpleSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for ArchimatchUser model.

    This serializer includes a subset of fields from the ArchimatchUser model for simplified serialization.

    Fields:
        first_name: First name of the user.
        last_name: Last name of the user.
        email: Email address of the user.
        phone_number: Phone number of the user.
    """

    class Meta:
        """
        Meta class for ArchimatchUserSimpleSerializer.

        Includes simplified fields for serialization and additional options.
        """

        model = ArchimatchUser
        fields = ["first_name", "last_name", "email", "phone_number"]
        extra_kwargs = {
            "email": {"required": True},
        }
