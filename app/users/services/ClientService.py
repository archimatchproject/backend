"""
Module: Client Service

This module defines the ClientService class that handles client-related operations such as login using email or phone number.

Classes:
    ClientService: Service class for client-related operations.

"""

import jwt
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.users.models import ArchimatchUser, Client
from app.users.serializers import ClientSerializer


class ClientService:
    """
    Service class for handling client-related operations such as login using email or phone number.

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
    def client_login_email(cls, request):
        """
        Authenticates a client using email and checks if they have set a password.

        Args:
            request (Request): Django request object containing client's email.

        Returns:
            Response: Response object with a message indicating if the client has set a password.

        Raises:
            APIException: If there are errors during client authentication.
        """
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"email"}
            cls.handle_user_data(request_keys, expected_keys)

            email = data.get("email")

            if Client.objects.filter(user__email=email).exists():
                user = ArchimatchUser.objects.get(username=email)
                if user.password == "":
                    response_data = {
                        "message": {"has_password": False},
                        "status_code": status.HTTP_200_OK,
                    }
                else:
                    response_data = {
                        "message": {"has_password": True},
                        "status_code": status.HTTP_200_OK,
                    }
            else:
                response_data = {
                    "message": "Client Not Found",
                    "status_code": status.HTTP_404_NOT_FOUND,
                }

            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)

    @classmethod
    def client_login_phone(cls, request):
        """
        Authenticates a client using phone number and checks if they have set a password.

        Args:
            request (Request): Django request object containing client's phone number.

        Returns:
            Response: Response object with a message indicating if the client has set a password and their email.

        Raises:
            APIException: If there are errors during client authentication.
        """
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"phone_number"}
            cls.handle_user_data(request_keys, expected_keys)

            phone_number = data.get("phone_number")

            if Client.objects.filter(user__phone_number=phone_number).exists():
                user = ArchimatchUser.objects.get(phone_number=phone_number)
                # TODO: SMS Code verification
                if user.password == "":
                    response_data = {
                        "message": {"has_password": False, "email": user.username},
                        "status_code": status.HTTP_200_OK,
                    }
                else:
                    response_data = {
                        "message": {"has_password": True, "email": user.username},
                        "status_code": status.HTTP_200_OK,
                    }
            else:
                response_data = {
                    "message": "Client Not Found",
                    "status_code": status.HTTP_404_NOT_FOUND,
                }

            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)
