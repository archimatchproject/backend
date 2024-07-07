"""
Module: Archimatch User Service

This module defines the ArchimatchUserService class that provides methods for handling user data
 and password creation.

Classes:
    ArchimatchUserService: Service class for handling user data and password creation.

"""

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.serializers.ArchimatchUserObtainPairSerializer import (
    ArchimatchUserObtainPairSerializer,
)
from app.users.serializers.ArchimatchUserPWSerializer import ArchimatchUserCreatePWSerializer
from app.users.serializers.ArchimatchUserPWSerializer import ArchimatchUserResetPWSerializer
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSimpleSerializer


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

        Raises:
            APIException: If there are errors in the password update process.
        """
        try:
            data = request.data
            serializer = ArchimatchUserCreatePWSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            email = validated_data.get("email")
            password = validated_data.get("password")
            confirm_password = validated_data.get("confirm_password")

            # Check if user exists
            if not ArchimatchUser.objects.filter(email=email).exists():
                raise ValidationError("User does not exist")

            user = ArchimatchUser.objects.get(email=email)

            # Set password if conditions are met
            if password == confirm_password:
                user.set_password(confirm_password)
                user.username = email
                user.save()

                # Generate tokens for the user
                tokens = cls.generate_tokens_for_user(email, password)
                return Response(
                    {
                        "message": "Password successfully updated",
                        "tokens": tokens,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                raise ValidationError("Passwords do not match")

        except ValidationError as e:
            raise e

        except Exception as e:
            raise APIException("Error creating password", str(e))

    @classmethod
    def archimatch_user_reset_password(cls, request):
        """
        Resest the password for a user based on provided data.

        Args:
            request (Request): Django request object containing user data.

        Returns:
            Response: Response object with a message indicating the status of the password update.

        Raises:
            APIException: If there are errors in the password update process.
        """
        try:
            data = request.data
            serializer = ArchimatchUserResetPWSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            # Check if user exists
            user = request.user
            old_password = validated_data.get("old_password")
            new_password = validated_data.get("new_password")
            confirm_new_password = validated_data.get("confirm_new_password")

            if not user.check_password(old_password):
                raise ValidationError("Incorrect old password")
            # Set new password if conditions are met
            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                return Response(
                    {"message": "Password successfully updated"},
                    status=status.HTTP_200_OK,
                )
            else:
                raise ValidationError("New passwords do not match")

        except ValidationError as e:
            raise e
        except Exception as e:
            raise APIException("Error resetting password", str(e))

    @classmethod
    def archimatch_user_update_data(cls, request):
        """
        Updates the basic data for a user based on provided data.
        """
        try:
            user = request.user
            data = request.data
            if not data:
                raise ValidationError("At least one field must be provided for update.")
            serializer = ArchimatchUserSimpleSerializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "User data successfully updated", "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            raise APIException("Error updating user data", str(e))
