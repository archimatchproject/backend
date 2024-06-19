"""
Module: Archimatch User Service

This module defines the ArchimatchUserService class that provides methods for handling user data and password creation.

Classes:
    ArchimatchUserService: Service class for handling user data and password creation.

Exceptions:
    APIException: Raised for API-related errors.

Modules Required:
    - rest_framework: Django REST framework for handling web APIs.
    - app.users.models.ArchimatchUser: Model representing users in the Archimatch application.
"""

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.users.models import ArchimatchUser


class ArchimatchUserService:
    """
    Service class for handling user data and password creation in the Archimatch application.

    Methods:
        handle_user_data(request_keys, expected_keys):
            Validates the presence of expected keys in request data.

        create_password(request):
            Creates or updates the password for a user based on provided data.
    """

    @classmethod
    def handle_user_data(cls, request_keys, expected_keys):
        """
        Validates the presence of expected keys in request data.

        Args:
            request_keys (set): Set of keys present in the request data.
            expected_keys (set): Set of keys expected to be present in the request data.

        Raises:
            APIException: If any expected key is missing in the request data.
        """
        if not expected_keys.issubset(request_keys):
            missing_keys = expected_keys - request_keys
            raise APIException(f"Missing keys: {', '.join(missing_keys)}")

    @classmethod
    def create_password(cls, request):
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
            request_keys = set(data.keys())
            expected_keys = {"id", "password", "confirm_password"}
            ArchimatchUserService.handle_user_data(request_keys, expected_keys)

            # Check if user with given id exists
            if not ArchimatchUser.objects.filter(id=data.get("id")).exists():
                raise APIException("This user does not exist")

            user = ArchimatchUser.objects.get(id=data.get("id"))
            password = data.get("password")
            confirm_password = data.get("confirm_password")

            # Update password if confirm_password matches and user doesn't have a password already
            if password == confirm_password and user.password == "":
                user.set_password(confirm_password)
                user.save()
            else:
                raise APIException("You already have a password")

            response_data = {
                "message": "Password successfully updated",
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)
