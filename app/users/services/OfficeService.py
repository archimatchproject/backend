"""
Module: Office Service

This module defines the OfficeService class that handles office-related operations such as
signup, login, and profile updates.

Classes:
    OfficeService: Service class for office-related operations.
"""

from django.utils.translation import get_language_from_request

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


from app.core.pagination import CustomPagination

from app.email_templates.signals import api_success_signal
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.Office import Office

from app.users.serializers.OfficeSerializer import (
    OfficeInputSerializer,
    OfficePersonalInformationSerializer,
    OfficeSerializer,
)

from app.users.serializers.UserAuthSerializer import UserAuthSerializer
from app.users.utils import generate_password_reset_token
from app.users.utils import validate_password_reset_token
from project_core.django import base as settings
from app.users.controllers.OfficeFilter import OfficeFilter
from app.users.models.SupplierSocialMedia import SupplierSocialMedia
from app.users.serializers.SupplierSocialMediaSerializer import SupplierSocialMediaSerializer


class OfficeService:
    """
    Service class for handling office-related operations such as signup, login, and
    profile updates.

    Attributes:
        serializer_class (Serializer): Serializer class for the Office model.

    """

    serializer_class = OfficeSerializer
    pagination_class = CustomPagination

    @classmethod
    def office_signup(cls, request):
        """
        Registers a new office in the system.

        Args:
            request (Request): Django request object containing office's email.

        Returns:
            Response: Response object indicating success or failure of office registration.
        """

        data = request.data
        email = data.get("email")

        if not email:
            raise APIException(detail="Email is required", code="validation_error")

        if ArchimatchUser.objects.filter(email=email).exists():
            raise APIException(
                detail="User with this email already exists", code="validation_error"
            )
        user = ArchimatchUser.objects.create(
            email=email,
            username=email,
            user_type="Office",
        )
        Office.objects.create(user=user)

        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        language_code = get_language_from_request(request)
        token = generate_password_reset_token(user.id)
        url = f"{settings.BASE_FRONTEND_URL}/{language_code}"
        reset_link = f"{url}/office/login/first-login-password/{token}"

        signal_data = {
            "template_name": "supplier_invite.html",
            "context": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": email,
                "reset_link": reset_link,
            },
            "to_email": email,
            "subject": "Archimatch Invite Office",
            "images": email_images,
        }
        api_success_signal.send(sender=cls, data=signal_data)

        return True, "Office successfully created"

    @classmethod
    def office_login(cls, request):
        """
        Authenticates an office using email and checks if they have set a password.

        Args:
            request (Request): Django request object containing office's email.

        Returns:
            Response: Response object with a message indicating if the office has set a password.

        Raises:
            serializers.ValidationError: If there are errors during office authentication.
        """

        data = request.data
        serializer = UserAuthSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")

        if not Office.objects.filter(user__email=email).exists():
            raise NotFound(detail="Office not found.")

        user = ArchimatchUser.objects.get(email=email)
        has_password = user.password != ""

        return True, {"has_password": has_password, "email": user.email}

    @classmethod
    def office_get_all(cls, request):
        """
        Handle GET request and return paginated Office objects with related OfficeRequest data.

        Args:
            request (HttpRequest): The incoming HTTP request object containing
                pagination parameters like page number, page size, etc.

        Returns:
            Response: A paginated response containing serialized combined
            data of Office and OfficeRequest.
        """

        queryset = Office.objects.all().order_by("created_at")
        # Apply filters using the SupplierFilter class
        filtered_queryset = OfficeFilter(request.GET, queryset=queryset).qs

        # Instantiate the paginator
        paginator = cls.pagination_class()

        # Apply pagination to the filtered queryset
        page = paginator.paginate_queryset(filtered_queryset, request)
        if page is not None:
            serializer = OfficeSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = OfficeSerializer(filtered_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def delete_office(cls, pk):
        """
        Deletes a office from the system.

        Args:
            request (Request): Django request object.
            office_id (int): ID of the office to be deleted.

        Returns:
            Response: Response object indicating success or failure of the office deletion.
        """

        office = Office.objects.get(id=pk)
        office.delete()
        return True, "Office successfully deleted"

    @classmethod
    def office_validate_password_token(cls, request):
        """
        validate password token
        """

        data = request.data
        token = data.get("token", False)
        if not token:
            raise serializers.ValidationError(detail="token is required")

        user_id, error = validate_password_reset_token(token)
        if error:
            raise APIException(detail=error)
        office = Office.objects.get(user__id=user_id)
        serializer = OfficeSerializer(office)
        return True, serializer.data

    @classmethod
    def office_get_accepted_list(cls, request):
        """
        Handle GET request and return paginated Office objects.
        This method retrieves all Office objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination parameters are not provided correctly or if an
        error occurs during serialization or database access, it returns a 400 Bad
        Request response with an appropriate error message.
        Args:
            request (HttpRequest): The incoming HTTP request object containing
                pagination parameters like page number, page size, etc.
        Returns:
            Response: A paginated response containing serialized Office objects
                or a 400 Bad Request response with an error message.
        """

        queryset = Office.objects.exclude(profile_image__isnull=True).exclude(profile_image="")
        # Apply filters using the OfficeFilter class
        filtered_queryset = OfficeFilter(request.GET, queryset=queryset).qs

        # Instantiate the paginator
        paginator = cls.pagination_class()

        # Apply pagination to the filtered queryset
        page = paginator.paginate_queryset(filtered_queryset, request)
        if page is not None:
            serializer = OfficeSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = OfficeSerializer(filtered_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def office_resend_email(cls, pk, request):
        """
        Resends the office invitation email.

        Args:
            pk (int): Primary key of the office.

        Returns:
            Tuple[bool, str]: Response indicating success or failure of email resend.
        """

        office = Office.objects.get(id=pk)
        email_images = settings.REFUSE_ARCHITECT_REQUEST_IMAGES
        token = generate_password_reset_token(office.user.id)
        language_code = get_language_from_request(request)
        url = f"{settings.BASE_FRONTEND_URL}/{language_code}"
        reset_link = f"{url}/office/login/first-login-password/{token}"

        signal_data = {
            "template_name": "supplier_invite.html",
            "context": {
                "first_name": office.office_name,
                "last_name": office.office_name,
                "email": office.user.email,
                "reset_link": reset_link,
            },
            "to_email": office.user.email,
            "subject": "Archimatch Invite Office",
            "images": email_images,
        }
        api_success_signal.send(sender=cls, data=signal_data)

        return True, "Email resent successfully"

    @classmethod
    def office_first_connection(cls, request):
        """
        Updates an office's initial profile information including office details and address.

        Args:
            request (Request): Django request object containing office's profile data.

        Returns:
            Response: Response object indicating success or failure of the profile update.

        Raises:
            serializers.ValidationError: If there are errors during office profile update.
        """

        data = request.data
        office_serializer = OfficeInputSerializer(data=data)
        office_serializer.is_valid(raise_exception=True)

        email = data.pop("email")
        if not Office.objects.filter(user__email=email).exists():
            raise NotFound(detail="Office not found.", code=status.HTTP_404_NOT_FOUND)

        office = Office.objects.get(user__email=email)
        phone_number = data.pop("phone_number")

        # Update user data
        user = office.user
        user.phone_number = phone_number
        user.save()

        # Update office model fields
        office_name = data.pop("office_name")
        office_address = data.pop("office_address")
        office_identifier = data.pop("office_identifier")
        is_public = data.pop("is_public", True)
        profile_image = data.pop("profile_image", None)

        # Update office data
        office.office_name = office_name
        office.office_address = office_address
        office.office_identifier = office_identifier
        office.is_public = is_public
        if profile_image:
            office.profile_image = profile_image

        # Save changes to office
        office.save()

        return True, "Office successfully updated."

    @classmethod
    def office_update_profile(cls, request):
        """
        Updates an office's profile information, including profile image.

        Args:
            request (Request): Django request object containing office's profile data.

        Returns:
            tuple: (bool, str) indicating success or failure message.
        """

        data = request.data

        # Validate the incoming data with the serializer
        serializer = OfficePersonalInformationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user_id = request.user.id
        office = Office.objects.get(user__id=user_id)
        user_data = validated_data.pop("user")
        phone_number = user_data.pop("phone_number")

        # Update user data
        user = office.user
        user.phone_number = phone_number
        user.save()

        # Update office data
        for attr, value in validated_data.items():
            setattr(office, attr, value)

        # Handle profile image upload
        if "profile_image" in request.FILES:
            office.profile_image = request.FILES["profile_image"]

        office.save()

        return True, "Office profile updated"

    @classmethod
    def office_update_social_links(cls, request):
        """
        Updates an office's social media links.

        Args:
            request (Request): Django request object containing office's social media data.

        Returns:
            tuple: (bool, str) indicating success or failure message for social media links update.

        Raises:
            APIException: If there are errors during social media links update.
        """

        data = request.data
        user_id = request.user.id

        # Validate incoming social media data
        social_media_serializer = SupplierSocialMediaSerializer(data=data)
        social_media_serializer.is_valid(raise_exception=True)

        validated_data = social_media_serializer.validated_data

        # Retrieve the office associated with the user
        office = Office.objects.get(user__id=user_id)

        # If the office does not have existing social media links, create them
        if not office.social_links:
            social_links, created = SupplierSocialMedia.objects.update_or_create(**validated_data)
            office.social_links = social_links
            office.save()
        else:
            # If the office already has social media links, update the existing record
            social_links = office.social_links
            SupplierSocialMedia.objects.filter(id=social_links.id).update(**validated_data)

        return True, "Office social media links successfully updated"

    @classmethod
    def office_get_profile(cls, request):
        """
        Retrieves office information.

        Returns:
            Response: Response object containing office object.
        """
        user_id = request.user.id
        if not Office.objects.filter(user__id=user_id).exists():
            raise NotFound(detail="Office not found.", code=status.HTTP_404_NOT_FOUND)
        office = Office.objects.get(user__id=user_id)
        office_serializer = OfficeSerializer(office)
        return True, office_serializer.data

    @classmethod
    def office_update_profile_image(cls, request):
        """
        Updates an Office's profile image.

        Args:
            request (Request): Django request object containing Office's profile image data.

        Returns:
            tuple: (success flag, message)
        """
        data = request.data
        user_id = request.user.id
        profile_image = data.get("profile_image", False)
        if not profile_image:
            raise serializers.ValidationError(detail="profile image is required")

        office = Office.objects.get(user__id=user_id)
        office.profile_image = profile_image
        user = office.user
        user.image = profile_image
        user.save()
        office.save()

        return True, "Office profile image successfully updated"
