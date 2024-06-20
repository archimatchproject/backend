"""
Module: Supplier Service

This module defines the SupplierService class that handles supplier-related operations such as signup, login, and profile updates.

Classes:
    SupplierService: Service class for supplier-related operations.
"""

import jwt
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.users.models import ArchimatchUser, Supplier
from app.users.models.SupplierSocialMedia import SupplierSocialMedia
from app.users.serializers import SupplierSerializer


class SupplierService:
    """
    Service class for handling supplier-related operations such as signup, login, and profile updates.

    Attributes:
        serializer_class (Serializer): Serializer class for the Supplier model.

    """

    serializer_class = SupplierSerializer

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
    def supplier_signup(cls, request):
        """
        Registers a new supplier in the system.

        Args:
            request (Request): Django request object containing supplier's email.

        Returns:
            Response: Response object indicating success or failure of supplier registration.
        """
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"email"}
            cls.handle_user_data(request_keys, expected_keys)

            email = data.get("email")

            if not Supplier.objects.filter(user__email=email).exists():
                user = ArchimatchUser.objects.create(email=email, username=email)
                supplier = Supplier.objects.create(user=user)
                user.save()
                supplier.save()

                response_data = {
                    "message": "Supplier_Created",
                    "status_code": status.HTTP_201_CREATED,
                }
            else:
                response_data = {
                    "message": "Supplier_Exists",
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                }

            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)

    @classmethod
    def supplier_login(cls, request):
        """
        Authenticates a supplier using email and checks if they have set a password.

        Args:
            request (Request): Django request object containing supplier's email.

        Returns:
            Response: Response object with a message indicating if the supplier has set a password.

        Raises:
            APIException: If there are errors during supplier authentication.
        """
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"email"}
            cls.handle_user_data(request_keys, expected_keys)

            email = data.get("email")

            if Supplier.objects.filter(user__email=email).exists():
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
                    "message": "Supplier Not Found",
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
    def supplier_first_connection(cls, request):
        """
        Updates a supplier's initial profile information including company details and phone number.

        Args:
            request (Request): Django request object containing supplier's profile data.

        Returns:
            Response: Response object indicating success or failure of the profile update.

        Raises:
            APIException: If there are errors during supplier profile update.
        """
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {
                "type",
                "company_name",
                "address",
                "phone_number",
                "speciality",
                "id",
            }
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                raise APIException("ce fournisseur n'existe pas")

            supplier = Supplier.objects.get(id=data.get("id"))
            phone_number = data.pop("phone_number")
            # update user data
            user = supplier.user
            user.phone_number = phone_number
            user.save()

            Supplier.objects.filter(id=data.get("id")).update(**data)

            response_data = {
                "message": "Supplier successfully updated",
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)

    @classmethod
    def supplier_update_profile(cls, request):
        """
        Updates a supplier's profile information excluding general settings and social media links.

        Args:
            request (Request): Django request object containing supplier's profile data.

        Returns:
            Response: Response object indicating success or failure of the profile update.

        Raises:
            APIException: If there are errors during supplier profile update.
        """
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {
                "company_name",
                "address",
                "phone_number",
                "speciality",
                "id",
            }
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                raise APIException("ce fournisseur n'existe pas")

            supplier = Supplier.objects.get(id=data.get("id"))
            phone_number = data.pop("phone_number")
            # update user data
            user = supplier.user
            user.phone_number = phone_number
            user.save()

            Supplier.objects.filter(id=data.get("id")).update(**data)

            response_data = {
                "message": "Supplier successfully updated",
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)

    @classmethod
    def supplier_update_general_settings(cls, request):
        """
        Updates a supplier's general settings such as bio or other preferences.

        Args:
            request (Request): Django request object containing supplier's settings data.

        Returns:
            Response: Response object indicating success or failure of the settings update.

        Raises:
            APIException: If there are errors during supplier settings update.
        """
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"bio", "id"}
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                raise APIException("ce fournisseur n'existe pas")

            Supplier.objects.filter(id=data.get("id")).update(**data)

            response_data = {
                "message": "Supplier successfully updated",
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)

    @classmethod
    def supplier_update_links(cls, request):
        """
        Updates a supplier's social media links.

        Args:
            request (Request): Django request object containing supplier's social media data.

        Returns:
            Response: Response object indicating success or failure of the social media links update.

        Raises:
            APIException: If there are errors during social media links update.
        """
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {"facebook", "instagram", "website", "id"}
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                raise APIException("ce fournisseur n'existe pas")

            supplier = Supplier.objects.get(id=data.get("id"))
            data.pop("id")
            if not supplier.social_links:
                supplier.social_links = SupplierSocialMedia.objects.create(**data)
                supplier.save()
            else:
                social_links = supplier.social_links
                SupplierSocialMedia.objects.filter(id=social_links.id).update(**data)

            response_data = {
                "message": "Supplier successfully updated",
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"), status=response_data.get("status_code")
            )
        except APIException as e:
            return Response({"message": str(e)}, status=e.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_410_GONE)
