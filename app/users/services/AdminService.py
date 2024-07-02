"""
Module containing AdminService class.

This module provides service methods for handling admin users, including creation,
updating, decoding tokens, retrieving admin by user ID, retrieving admin by token,
handling user data validation, and admin login authentication.

Classes:
    AdminService: Service class for admin user operations.
"""

import environ
import jwt

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.users.models import Admin
from app.users.serializers import AdminSerializer


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
        try:
            serializer = AdminSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return cls.handle_exception(e)

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
        try:
            serializer = AdminSerializer(instance, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return cls.handle_exception(e)

    @classmethod
    def decode_token(cls, token):
        """
        Decodes the provided JWT token using the SECRET_KEY environment variable.

        Args:
            token (str): JWT token string to decode.

        Returns:
            dict: Decoded payload from the JWT token.
        """
        try:
            payload = jwt.decode(
                token,
                env("SECRET_KEY"),
                algorithms=["HS256"],
            )
            return payload
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}
        except Exception:
            return {"error": "Error decoding token"}

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
        except Admin.DoesNotExist:
            return None
        except Exception as e:
            return cls.handle_exception(e)

    @classmethod
    def retrieve_by_token(cls, request):
        """
        Retrieves an admin user based on the JWT token extracted from the request.

        Args:
            request (Request): HTTP request object containing the authorization token.

        Returns:
            Response: HTTP response containing serialized admin data or error message.
        """
        try:
            auth_header = request.META.get("HTTP_AUTHORIZATION")

            if not auth_header or not auth_header.startswith("Bearer "):
                return Response(
                    {"error": "Invalid token format"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            token = auth_header.split(" ")[1]
            payload = cls.decode_token(token)

            if "error" in payload:
                return Response(
                    {"error": payload["error"]},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            user_id = payload.get("user_id")
            if user_id:
                admin = cls.get_admin_by_user_id(user_id)
                if admin:
                    serializer = AdminSerializer(admin)
                    return Response(serializer.data)
                return Response(
                    {"error": "Admin not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {"error": "Token decoded successfully but no user ID found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return cls.handle_exception(e)

    @classmethod
    def handle_user_data(cls, request_keys, expected_keys):
        """
        Validates the presence of expected keys in the request data.

        Args:
            request_keys (set): Set of keys present in the request data.
            expected_keys (set): Set of expected keys that should be present.

        Raises:
            APIException: If any expected keys are missing in the request data.
        """
        if not expected_keys.issubset(request_keys):
            missing_keys = expected_keys - request_keys
            raise APIException(f"Missing keys: {', '.join(missing_keys)}")

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
            request_keys = set(data.keys())
            expected_keys = {"email"}
            cls.handle_user_data(request_keys, expected_keys)

            email = data.get("email")

            if Admin.objects.filter(user__email=email).exists():
                response_data = {
                    "message": "Admin Found",
                    "status_code": status.HTTP_200_OK,
                }
            else:
                response_data = {
                    "message": "Admin Not Found",
                    "status_code": status.HTTP_404_NOT_FOUND,
                }

            return Response(
                response_data.get("message"),
                status=response_data.get("status_code"),
            )
        except APIException as e:
            return Response(
                {"message": str(e)},
                status=e.status_code,
            )
        except Exception:
            return Response(
                {"message": "An error occurred during admin login"},
                status=status.HTTP_410_GONE,
            )

    @classmethod
    def handle_exception(cls, e):
        """
        Handles exceptions by returning a formatted error response.

        Args:
            e (Exception): The exception that was raised.

        Returns:
            Response: HTTP response containing the error message.
        """
        return Response(
            {"message": "An internal error occurred"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
