"""
Module containing ArchimatchUserSerializer and ArchimatchUserSimpleSerializer classes.

This module provides serializers for the ArchimatchUser model, tailored for different use cases.

Classes:
    ArchimatchUserSerializer: Detailed serializer for ArchimatchUser model.
    ArchimatchUserSimpleSerializer: Simplified serializer for ArchimatchUser model.
"""

from fcm_django.models import FCMDevice
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

    device_id = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for ArchimatchUserSerializer.

        Includes detailed fields for serialization and additional options.
        """

        model = ArchimatchUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "image",
            "user_type",
            "is_deleted",
            "is_suspended",
            "suspension_start_date",
            "suspension_end_date",
            "device_id",
        ]
        extra_kwargs = {
            "username": {"read_only": True},
        }
        read_only_fields = [
            "is_deleted",
            "is_suspended",
            "suspension_start_date",
            "suspension_end_date",
        ]

    def get_device_id(self, obj):
        """
        Get the FCMDevice ID associated with the architect's user.
        """
        fcm_device = FCMDevice.objects.filter(user=obj).first()
        return fcm_device.id if fcm_device else None


class ArchimatchUserSimpleSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for ArchimatchUser model.

    This serializer includes a subset of fields from the ArchimatchUser model for
    simplified serialization.

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
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "phone_number": {"required": True},
        }


class ArchimatchUserEmailPhoneSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for ArchimatchUser model.

    This serializer includes a subset of fields from the ArchimatchUser model for
    simplified serialization.

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
        fields = [
            "email",
            "phone_number",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "phone_number": {"required": True},
        }
