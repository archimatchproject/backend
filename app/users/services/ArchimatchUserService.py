"""
Module: Archimatch User Service

This module defines the ArchimatchUserService class that provides methods for handling user data
 and password creation.

Classes:
    ArchimatchUserService: Service class for handling user data and password creation.

"""

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.serializers.ArchimatchUserObtainPairSerializer import (
    ArchimatchUserObtainPairSerializer,
)


class ArchimatchUserService:
    """
    Service class for handling user data and password creation in the Archimatch application.


    """

    def generate_tokens_for_user(email, password):
        """
        Generates token for user
        """
        serializer = ArchimatchUserObtainPairSerializer(
            data={
                "email": email,
                "password": password,
            }
        )
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @classmethod
    def archimatch_user_create_password(cls, request):
        """
        Creates or updates the password for a user based on provided data.

        Args:
            request (Request): Django request object containing user data.

        Returns:
            Response: Response object with a message indicating the status of the password update.
        """
        try:
            data = request.data
            # Validate input keys

            req_email = data.get("email")
            if req_email is None:
                raise serializers.ValidationError(detail="Email is required")

            # Check if user exists
            if not ArchimatchUser.objects.filter(email=req_email).exists():
                raise NotFound(detail="User does not exist")

            user = ArchimatchUser.objects.get(email=req_email)
            password = data.get("password")
            confirm_password = data.get("confirm_password")

            # Validate passwords match
            if password != confirm_password:
                raise serializers.ValidationError(detail="Passwords do not match")

            # Update user password
            user.set_password(confirm_password)
            user.username = req_email
            user.save()

            # Generate tokens for the user
            tokens = cls.generate_tokens_for_user(req_email, password)

            response_data = {
                "message": "Password successfully updated",
                "tokens": tokens,
            }
            return Response(
                response_data,
                status=response_data["status_code"],
            )

        except APIException as e:
            raise e
        except Exception:
            raise APIException

    @classmethod
    def archimatch_user_reset_password(cls, request):
        """
        Resets the password for a user based on provided data.

        Args:
            request (Request): Django request object containing user data.

        Returns:
            Response: Response object with a message indicating the status of the password update.
        """
        try:
            data = request.data
            user_id = data.get("id", None)
            if id is None:
                raise serializers.ValidationError(detail="user id is required")
            # Check if user exists
            if not ArchimatchUser.objects.filter(id=user_id).exists():
                raise NotFound(detail="User does not exist")

            user = ArchimatchUser.objects.get(id=user_id)
            old_password = data.get("old_password")
            new_password = data.get("new_password")
            confirm_new_password = data.get("confirm_new_password")

            # Check if old password matches
            if not user.check_password(old_password):
                raise serializers.ValidationError(detail="Incorrect old password")

            # Validate new passwords match
            if new_password != confirm_new_password:
                raise serializers.ValidationError(detail="New passwords do not match")

            # Set new password
            user.set_password(new_password)
            user.save()

            response_data = {
                "message": "Password successfully updated",
            }
            return Response(
                response_data,
                status=status.HTTP_200_OK,
            )
        except NotFound as e:
            raise e
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))
