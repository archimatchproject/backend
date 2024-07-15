"""
Module containing AdminService class.

This module provides service methods for handling admin users, including creation,
updating, decoding tokens, retrieving admin by user ID, retrieving admin by token,
handling user data validation, and admin login authentication.

Classes:
    AdminService: Service class for admin user operations.
"""

from django.db import transaction

import environ

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from app.email_templates.signals import api_success_signal
from app.users import PERMISSION_CODENAMES
from app.users.models.Admin import Admin
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.serializers.AdminSerializer import AdminSerializer
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSimpleSerializer
from project_core.django import base as settings


env = environ.Env()


class AdminService:
    """
    Service class for admin user operations.

    This class provides methods to handle admin user-related operations such as
    creating admin users, updating admin user data, decoding tokens, retrieving
    admin users by various criteria, handling user data validation, and admin login.
    """

    @classmethod
    def create_admin(cls, data):
        """
        Creates a new admin user with the provided data.

        Args:
            data (dict): Dictionary containing data for creating the admin user.

        Returns:
            Response: HTTP response containing serialized admin data or errors.
        """

        admin_serializer = AdminSerializer(data=data)
        admin_serializer.is_valid(raise_exception=True)
        validated_data = admin_serializer.validated_data
        user_data = validated_data.pop("user")
        user_serializer = ArchimatchUserSimpleSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            rights = validated_data.pop("rights", [])
            user = ArchimatchUser.objects.create(**user_data)
            admin = Admin.objects.create(user=user, **validated_data)
            try:
                admin.set_permissions(rights)
            except serializers.ValidationError as e:
                raise serializers.ValidationError(e.detail)
            email_images = settings.ADD_ADMIN_IMAGES
            signal_data = {
                "template_name": "add_sub_admin.html",
                "context": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                },
                "to_email": user.email,
                "subject": "Refusing Architect Request",
                "images": email_images,
            }
            api_success_signal.send(sender=cls, data=signal_data)
            return Response(
                AdminSerializer(admin).data,
                status=status.HTTP_201_CREATED,
            )

    @classmethod
    def update_admin(cls, instance, data):
        """
        Updates an existing admin user instance with the provided data.

        Args:
            instance (Admin): Admin instance to update.
            data (dict): Dictionary containing updated data for the admin user.

        Returns:
            Response: HTTP response containing serialized admin data or errors.
        """

        # Extract and handle user data separately
        user_data = data.pop("user", {})
        email = user_data.pop("email", None)
        phone_number = user_data.pop("phone_number", None)

        admin_serializer = AdminSerializer(instance, data=data, partial=True)
        admin_serializer.is_valid(raise_exception=True)
        validated_data = admin_serializer.validated_data

        # Update user data if provided
        if email is not None:
            if email != instance.user.email:  # Check if email is changing
                if ArchimatchUser.objects.filter(email=email).exclude(id=instance.user.id).exists():
                    raise serializers.ValidationError("Email already exists.")
                instance.user.email = email

        if phone_number is not None:
            instance.user.phone_number = phone_number

        # Update any other user fields from user_data
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        instance.user.save()

        rights = validated_data.pop("rights", [])

        # Update admin instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update permissions
        instance.set_permissions(rights)

        return Response(
            AdminSerializer(instance).data,
            status=status.HTTP_200_OK,
        )

    @classmethod
    def get_all_permissions(cls):
        """
        Retrieves all permissions with their associated colors.

        Returns:
            Response: HTTP response containing all permissions and their colors.
        """
        permissions_with_colors = [
            {"right": right, "color": data["color"]} for right, data in PERMISSION_CODENAMES.items()
        ]
        return Response(permissions_with_colors, status=status.HTTP_200_OK)
