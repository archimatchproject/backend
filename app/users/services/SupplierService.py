"""
Module: Supplier Service

This module defines the SupplierService class that handles supplier-related operations such as
signup, login, and profile updates.

Classes:
    SupplierService: Service class for supplier-related operations.
"""

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.core.validation.exceptions import UserDataException
from app.users import APPEARANCES
from app.users.models import ArchimatchUser
from app.users.models import Supplier
from app.users.models.SupplierSocialMedia import SupplierSocialMedia
from app.users.models.SupplierSpeciality import SupplierSpeciality
from app.users.serializers import SupplierSerializer
from app.users.serializers.SupplierSpecialitySerializer import SupplierSpecialitySerializer


class SupplierService:
    """
    Service class for handling supplier-related operations such as signup, login, and
    profile updates.

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
            raise UserDataException(f"Missing keys: {', '.join(missing_keys)}")

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
                if not ArchimatchUser.objects.filter(email=email).exists():
                    user = ArchimatchUser.objects.create(
                        email=email,
                        username=email,
                        user_type="Supplier",
                    )
                    Supplier.objects.create(user=user)
                    response_data = {
                        "message": {"message": "supplier_created"},
                        "status_code": status.HTTP_201_CREATED,
                    }
                else:
                    response_data = {
                        "message": {"message": "user_exists"},
                        "status_code": status.HTTP_400_BAD_REQUEST,
                    }
            else:
                response_data = {
                    "message": {"message": "supplier_exists"},
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }

            return Response(
                response_data.get("message"),
                status=response_data.get("status_code"),
            )

        except UserDataException as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except APIException as e:
            return Response(
                {"message": str(e)},
                status=e.status_code,
            )

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
                        "message": {
                            "has_password": False,
                            "email": user.email,
                        },
                        "status_code": status.HTTP_200_OK,
                    }
                else:
                    response_data = {
                        "message": {
                            "has_password": True,
                            "email": user.email,
                        },
                        "status_code": status.HTTP_200_OK,
                    }
            else:
                response_data = {
                    "message": {"message": "supplier_not_found"},
                    "status_code": status.HTTP_404_NOT_FOUND,
                }

            return Response(
                response_data.get("message"),
                status=response_data.get("status_code"),
            )

        except UserDataException as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except APIException as e:
            return Response(
                {"message": str(e)},
                status=e.status_code,
            )

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
                "company_address",
                "company_speciality",
                "company_name",
                "phone_number",
                "speciality_type",
                "id",
                "appearance",
            }
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                response_data = {
                    "message": {"message": "supplier doesn't exist"},
                    "status_code": status.HTTP_404_NOT_FOUND,
                }
                return Response(
                    response_data.get("message"),
                    status=response_data.get("status_code"),
                )

            supplier = Supplier.objects.get(id=data.get("id"))
            phone_number = data.pop("phone_number")

            # Update user data
            user = supplier.user
            user.phone_number = phone_number
            user.save()

            # Update supplier data
            speciality_type_ids = data.pop("speciality_type")
            supplier.speciality_type.set(speciality_type_ids)

            Supplier.objects.filter(id=data.get("id")).update(**data)

            response_data = {
                "message": {"message": "supplier successfully updated"},
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"),
                status=response_data.get("status_code"),
            )

        except UserDataException as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except APIException as e:
            return Response(
                {"message": str(e)},
                status=e.status_code,
            )

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
                "company_address",
                "phone_number",
                "company_speciality",
                "id",
            }
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                response_data = {
                    "message": {"message": "supplier doesn't exist"},
                    "status_code": status.HTTP_404_NOT_FOUND,
                }
                return Response(
                    response_data.get("message"),
                    status=response_data.get("status_code"),
                )

            supplier = Supplier.objects.get(id=data.get("id"))
            phone_number = data.pop("phone_number")

            # Update user data
            user = supplier.user
            user.phone_number = phone_number
            user.save()

            # Update supplier data
            Supplier.objects.filter(id=data.get("id")).update(**data)

            response_data = {
                "message": {"message": "supplier successfully updated"},
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"),
                status=response_data.get("status_code"),
            )

        except UserDataException as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except APIException as e:
            return Response(
                {"message": str(e)},
                status=e.status_code,
            )

    @classmethod
    def supplier_update_bio(cls, request):
        """
        Updates a supplier's BIO such as bio or other preferences.

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
                response_data = {
                    "message": {"message": "Supplier doesn't exist"},
                    "status_code": status.HTTP_404_NOT_FOUND,
                }
                return Response(
                    response_data.get("message"),
                    status=response_data.get("status_code"),
                )

            Supplier.objects.filter(id=data.get("id")).update(bio=data.get("bio"))

            response_data = {
                "message": {"message": "Supplier bio successfully updated"},
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"),
                status=response_data.get("status_code"),
            )

        except UserDataException as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except APIException as e:
            return Response(
                {"message": str(e)},
                status=e.status_code,
            )

    @classmethod
    def supplier_update_presentation_video(cls, request):
        """
        Updates a supplier's Presentaion VIdeo such as bio or other preferences.

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
            expected_keys = {
                "presentation_video",
                "id",
            }
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                response_data = {
                    "message": {"message": "Supplier doesn't exist"},
                    "status_code": status.HTTP_404_NOT_FOUND,
                }
                return Response(
                    response_data.get("message"),
                    status=response_data.get("status_code"),
                )

            Supplier.objects.filter(id=data.get("id")).update(
                presentation_video=data.get("presentation_video")
            )

            response_data = {
                "message": {"message": "Supplier presentation video successfully updated"},
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"),
                status=response_data.get("status_code"),
            )

        except UserDataException as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except APIException as e:
            return Response(
                {"message": str(e)},
                status=e.status_code,
            )

    @classmethod
    def supplier_update_links(cls, request):
        """
        Updates a supplier's social media links.

        Args:
            request (Request): Django request object containing supplier's social media data.

        Returns:
            Response: Response object indicating success or failure of the social media links
            update.

        Raises:
            APIException: If there are errors during social media links update.
        """
        try:
            data = request.data
            request_keys = set(data.keys())
            expected_keys = {
                "facebook",
                "instagram",
                "website",
                "id",
            }
            cls.handle_user_data(request_keys, expected_keys)

            if not Supplier.objects.filter(id=data.get("id")).exists():
                response_data = {
                    "message": {"message": "Supplier doesn't exist"},
                    "status_code": status.HTTP_404_NOT_FOUND,
                }
                return Response(
                    response_data.get("message"),
                    status=response_data.get("status_code"),
                )

            supplier = Supplier.objects.get(id=data.get("id"))
            social_links_data = {
                "facebook": data.get("facebook"),
                "instagram": data.get("instagram"),
                "website": data.get("website"),
            }

            if not supplier.social_links:
                social_links, created = SupplierSocialMedia.objects.update_or_create(
                    **social_links_data
                )
                supplier.social_links = social_links
                supplier.save()
            else:
                social_links = supplier.social_links
                SupplierSocialMedia.objects.filter(id=social_links.id).update(**social_links_data)
                supplier.refresh_from_db()

            response_data = {
                "message": {"message": "Supplier social links successfully updated"},
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data.get("message"),
                status=response_data.get("status_code"),
            )

        except UserDataException as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except APIException as e:
            return Response(
                {"message": str(e)},
                status=e.status_code,
            )

    @classmethod
    def get_speciality_types(cls):
        """
        Retrieves all speciality types.

        Returns:
            Response: Response object containing the speciality types.
        """
        try:
            speciality_types = SupplierSpeciality.objects.all()
            speciality_types_data = SupplierSpecialitySerializer(speciality_types, many=True).data

            return Response(
                speciality_types_data,
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {"message": "Error retrieving speciality types"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @classmethod
    def get_appearances(cls):
        """
        Retrieves all appearances.

        Returns:
            Response: Response object containing the appearances.
        """
        try:
            appearances_data = APPEARANCES
            return Response(
                appearances_data,
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {"message": "Error retrieving appearances"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
