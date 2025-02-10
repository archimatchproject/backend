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

from app.users.serializers.OfficeSerializer import OfficeSerializer

from app.users.serializers.UserAuthSerializer import UserAuthSerializer
from app.users.utils import generate_password_reset_token
from app.users.utils import validate_password_reset_token
from project_core.django import base as settings
from app.users.controllers.OfficeFilter import OfficeFilter


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
