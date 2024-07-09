"""
Module: Supplier Service

This module defines the SupplierService class that handles supplier-related operations such as
signup, login, and profile updates.

Classes:
    SupplierService: Service class for supplier-related operations.
"""

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.email_templates.signals import api_success_signal
from app.users import APPEARANCES
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.Supplier import Supplier
from app.users.models.SupplierSocialMedia import SupplierSocialMedia
from app.users.models.SupplierSpeciality import SupplierSpeciality
from app.users.serializers.SupplierSerializer import SupplierInputSerializer
from app.users.serializers.SupplierSerializer import SupplierPersonalInformationSerializer
from app.users.serializers.SupplierSerializer import SupplierSerializer
from app.users.serializers.SupplierSocialMediaSerializer import SupplierSocialMediaSerializer
from app.users.serializers.SupplierSpecialitySerializer import SupplierSpecialitySerializer
from app.users.serializers.UserAuthSerializer import UserAuthSerializer
from project_core.django import base as settings


class SupplierService:
    """
    Service class for handling supplier-related operations such as signup, login, and
    profile updates.

    Attributes:
        serializer_class (Serializer): Serializer class for the Supplier model.

    """

    serializer_class = SupplierSerializer

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
            email = data.get("email")

            if email is None:
                raise serializers.ValidationError(detail="Email is required")

            if ArchimatchUser.objects.filter(email=email).exists():
                raise serializers.ValidationError(detail="User with this email already exists")

            user = ArchimatchUser.objects.create(
                email=email,
                username=email,
                user_type="Supplier",
            )
            Supplier.objects.create(user=user)

            response_data = {
                "message": "Supplier successfully created",
                "status_code": status.HTTP_201_CREATED,
            }

            return Response(
                response_data,
                status=response_data["status_code"],
            )

        except APIException as e:
            raise e
        except Exception:
            raise APIException(detail="error singing up supplier")

    @classmethod
    def supplier_login(cls, request):
        """
        Authenticates a supplier using email and checks if they have set a password.

        Args:
            request (Request): Django request object containing supplier's email.

        Returns:
            Response: Response object with a message indicating if the supplier has set a password.

        Raises:
            serializers.ValidationError: If there are errors during supplier authentication.
        """
        try:
            data = request.data
            serializer = UserAuthSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get("email")

            if not Supplier.objects.filter(user__email=email).exists():
                raise NotFound(detail="Supplier not found.")

            user = ArchimatchUser.objects.get(email=email)
            has_password = user.password != ""

            response_data = {
                "message": {
                    "has_password": has_password,
                    "email": user.email,
                },
                "status_code": status.HTTP_200_OK,
            }

            return Response(
                response_data,
                status=response_data["status_code"],
            )

        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(
                detail=str(e),
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
            serializers.ValidationError: If there are errors during supplier profile update.
        """
        try:
            data = request.data
            supplier_serializer = SupplierInputSerializer(data=data)
            supplier_serializer.is_valid(raise_exception=True)

            email = data.pop("email")
            if not Supplier.objects.filter(user__email=email).exists():
                raise NotFound(detail="Supplier not found.", code=status.HTTP_404_NOT_FOUND)

            supplier = Supplier.objects.get(user__email=email)
            phone_number = data.pop("phone_number")

            # Update user data
            user = supplier.user
            user.phone_number = phone_number
            user.save()

            # Update supplier data
            speciality_type_ids = data.pop("speciality_type")
            supplier.speciality_type.set(speciality_type_ids)

            # Update supplier model fields
            Supplier.objects.filter(user__email=email).update(**data)

            response_data = {
                "message": {"message": "Supplier successfully updated."},
                "status_code": status.HTTP_200_OK,
            }
            return Response(
                response_data,
                status=response_data.get("status_code"),
            )

        except serializers.ValidationError as e:
            raise e
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

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
            serializer = SupplierPersonalInformationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user_id = request.user.id
            supplier = Supplier.objects.get(user__id=user_id)

            phone_number = data.pop("phone_number")

            # Update user data
            user = supplier.user
            user.phone_number = phone_number
            user.save()

            # Update supplier data
            for attr, value in data.items():
                setattr(supplier, attr, value)
            supplier.save()

            response_data = {
                "message": "supplier successfully updated",
            }
            return Response(
                response_data,
                status=status.HTTP_200_OK,
            )
        except Supplier.DoesNotExist:
            raise NotFound(detail="Supplier not found.")
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

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
            user_id = request.user.id
            bio = data.get("bio", None)

            if bio is None:
                raise serializers.ValidationError(detail="Bio is required")

            supplier = Supplier.objects.get(user__id=user_id)
            supplier.bio = bio
            supplier.save()

            response_data = {
                "message": "Supplier bio successfully updated",
            }
            return Response(
                response_data,
                status=status.HTTP_200_OK,
            )
        except Supplier.DoesNotExist:
            raise NotFound(detail="Supplier not found.")
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

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
            user_id = request.user.id
            presentation_video = data.get("presentation_video", None)
            if presentation_video is None:
                raise serializers.ValidationError(detail="presentation video is required")

            supplier = Supplier.objects.get(user__id=user_id)
            supplier.presentation_video = presentation_video
            supplier.save()

            response_data = {"message": "Supplier presentation video successfully updated"}
            return Response(response_data.get("message"), status=status.HTTP_200_OK)

        except Supplier.DoesNotExist:
            raise NotFound(detail="Supplier not found.")
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

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
            user_id = request.user.id

            social_media_serializer = SupplierSocialMediaSerializer(data=data)
            social_media_serializer.is_valid(raise_exception=True)

            validated_data = social_media_serializer.validated_data

            supplier = Supplier.objects.get(user__id=user_id)

            if not supplier.social_links:
                social_links, created = SupplierSocialMedia.objects.update_or_create(
                    **validated_data
                )
                supplier.social_links = social_links
                supplier.save()
            else:
                social_links = supplier.social_links
                SupplierSocialMedia.objects.filter(id=social_links.id).update(**validated_data)

            response_data = {"message": "Supplier social links successfully updated"}
            return Response(
                response_data.get("message"),
                status=status.HTTP_200_OK,
            )

        except Supplier.DoesNotExist:
            raise NotFound(detail="Supplier not found.")
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

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
            raise APIException(
                detail="Error retrieving speciality types",
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
            raise APIException(
                detail="Error retrieving appearances",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @classmethod
    def supplier_get_profile(cls, request):
        """
        Retrieves supplier information.

        Returns:
            Response: Response object containing supplier object.
        """
        user_id = request.user.id
        print(user_id)
        try:
            if not Supplier.objects.filter(user__id=user_id).exists():
                raise NotFound(detail="Supplier not found.", code=status.HTTP_404_NOT_FOUND)
            supplier = Supplier.objects.get(user__id=user_id)
            supplier_serializer = SupplierSerializer(supplier)
            return Response(
                supplier_serializer.data,
                status=status.HTTP_200_OK,
            )
        except APIException as e:
            raise e
        except Exception as e:
            raise APIException(detail=str(e))

    @classmethod
    def supplier_send_reset_password_link(cls, request):
        """
        send reset password link for suppliers.


        """
        try:
            data = request.data
            serializer = UserAuthSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get("email")

            supplier = Supplier.objects.get(user__email=email)
            email_images = settings.COMMON_IMAGES + settings.ARCHITECT_PASSWORD_IMAGES
            context = {
                "first_name": supplier.user.first_name,
                "last_name": supplier.user.last_name,
                "email": data.get("email"),
                "reset_link": "www.google.com",
            }
            signal_data = {
                "template_name": "architect_reset_password.html",
                "context": context,
                "to_email": data.get("email"),
                "subject": "Supplier Reset Password",
                "images": email_images,
            }
            api_success_signal.send(sender=cls, data=signal_data)
            return Response(
                {"message": "email sent successfully"},
                status=status.HTTP_200_OK,
            )
        except Supplier.DoesNotExist:
            raise NotFound(detail="Supplier not found")
        except Exception as e:
            raise APIException(
                detail=str(e),
            )
