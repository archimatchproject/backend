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
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.email_templates.signals import api_success_signal
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
            signal_data = {
                "template_name": "architect_request.html",
                "context": {"reset_link": "google.com"},
                "to_email": "ghazichaftar.pfe@gmail.com",
                "subject": "Architect Account Creation",
                "images": settings.COMMON_IMAGES,
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

        user_data = data.pop("user", {})
        email = user_data.pop("email", None)
        phone_number = user_data.pop("phone_number", None)

        admin_serializer = AdminSerializer(instance, data=data, partial=True)
        admin_serializer.is_valid(raise_exception=True)
        validated_data = admin_serializer.validated_data

        # Update user data
        if email is not None:
            user_data["email"] = email
        if phone_number is not None:
            user_data["phone_number"] = phone_number

        ArchimatchUser.objects.filter(id=instance.user.id).update(**user_data)

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
    def get_admin_by_user_id(cls, user_id):
        """
        Retrieves an admin user based on the provided user ID.

        Args:
            user_id (int): ID of the user associated with the admin user.

        Returns:
            Admin: Admin object associated with the provided user ID.
        """
        try:
            admin = Admin.objects.get(user__id=user_id)
            return admin
        except Admin.DoesNotExist as e:
            return APIException(detail=str(e))
        except Exception as e:
            raise APIException(detail=str(e))

    @classmethod
    def admin_login(cls, request):
        """
        Authenticates an admin user based on the provided email address.

        Args:
            request (Request): HTTP request object containing the email address.

        Returns:
            Response: HTTP response indicating the status of the admin login attempt.
        """
        try:
            data = request.data

            email = data.get("email")
            if email is None:
                raise serializers.ValidationError(detail="email is required")

            if not Admin.objects.filter(user__email=email).exists():
                raise NotFound(detail="Admin not found")

            response_data = {
                "message": "Admin Found",
                "status_code": status.HTTP_200_OK,
            }

            return Response(
                response_data.get("message"),
                status=response_data.get("status_code"),
            )
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))
