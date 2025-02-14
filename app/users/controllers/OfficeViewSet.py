"""
Module: app.views.office

This module provides view classes for interacting with Office instances
using Django REST Framework, including custom actions for signup, login,
and profile management.
"""

from rest_framework import viewsets
from rest_framework.decorators import action

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.users.models.Office import Office
from app.users.serializers.OfficeSerializer import OfficeInputSerializer, OfficeSerializer
from app.users.serializers.UserAuthSerializer import UserAuthSerializer
from app.users.services.OfficeService import OfficeService
from rest_framework import status


class OfficeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for interacting with Office instances.

    This ViewSet provides standard CRUD operations for Office instances,
    along with custom actions for signup, login, and profile management.
    """

    serializer_class = OfficeSerializer
    queryset = Office.objects.all()

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="signup",
        serializer_class=UserAuthSerializer,
    )
    @handle_service_exceptions
    def office_signup(self, request):
        """
        Allows an office to sign up using a custom action.

        Args:
            self (OfficeViewSet): Instance of the OfficeViewSet class.
            request (Request): HTTP request object containing signup data.

        Returns:
            Response: Response indicating success or failure of the signup attempt.
        """
        success, message = OfficeService.office_signup(request)
        return build_response(success=success, message=message, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="login",
        serializer_class=UserAuthSerializer,
    )
    @handle_service_exceptions
    def office_login(self, request):
        """
        Allows an office to login using a custom action.

        Args:
            self (OfficeViewSet): Instance of the OfficeViewSet class.
            request (Request): HTTP request object containing login data.

        Returns:
            Response: Response indicating success or failure of the login attempt.
        """
        success, office_data = OfficeService.office_login(request)
        return build_response(success=success, data=office_data, status=status.HTTP_200_OK)

    def get(self, request):
        """
        Retrieve all offices.

        This method allows retrieval of all Office objects from the database.
        It delegates the actual retrieval to the `office_get_all` class method
        of `OfficeService`, which handles pagination and serialization.

        Args:
            self (OfficeViewSet): Instance of the OfficeViewSet class.
            request (Request): HTTP GET request object.

        Returns:
            Response: A paginated response containing serialized Supplier objects
                or an error response if there's a problem during retrieval.
        """
        return OfficeService.office_get_all(request)

    @handle_service_exceptions
    def delete(self, request, pk=None):
        """
        Deletes an office from the system.

        Args:
            request (Request): Django request object.
            pk (int): ID of the office to be deleted.

        Returns:
            Response: Response object indicating success or failure of the office deletion.
        """
        success, message = OfficeService.delete_office(pk)
        return build_response(success=success, message=message, status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="validate-password-token",
        url_name="validate-password-token",
    )
    @handle_service_exceptions
    def office_validate_password_token(self, request):
        """
        sends Office reset password email.

        Args:
            self (OfficeViewSet): Instance of the OfficeViewSet class.
            request (Request): HTTP request object.
        """
        success, profile_data = OfficeService.office_validate_password_token(request)
        return build_response(success=success, data=profile_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["POST"],
        url_path="resend-email",
    )
    @handle_service_exceptions
    def office_resend_email(self, request, pk=None):
        """
        Custom action to resend email to office

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the office object

        Returns:
            Response: The response object containing the result of the operation.
        """
        success, message = OfficeService.office_resend_email(pk, request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="first-connection",
        serializer_class=UserAuthSerializer,
    )
    @handle_service_exceptions
    def office_first_cnx(self, request):
        """
        Handles the first connection setup for an office using a custom action.

        Args:
            request (Request): HTTP request object containing first connection data.

        Returns:
            Response: Response indicating success or failure of the first connection attempt.
        """
        success, message = OfficeService.office_first_connection(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="get-profile",
        url_name="get-profile",
    )
    @handle_service_exceptions
    def office_get_profile(self, request):
        """
        Retrieves office profile details.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing office details.
        """
        success, profile_data = OfficeService.office_get_profile(request)
        return build_response(success=success, data=profile_data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["PUT"],
        permission_classes=[],
        url_path="update-profile",
        serializer_class=OfficeInputSerializer,
    )
    @handle_service_exceptions
    def office_update_profile(self, request):
        """
        Allows an office to update its profile information using a custom action.

        Args:
            self (OfficeViewSet): Instance of the OfficeViewSet class.
            request (Request): HTTP request object containing profile update data.

        Returns:
            Response: Response indicating success or failure of the profile update attempt.
        """
        success, message = OfficeService.office_update_profile(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["PUT"],
        permission_classes=[],
        url_path="update-links",
    )
    @handle_service_exceptions
    def office_update_links(self, request):
        """
        Allows an office to update their social media links using a custom action.

        Args:
            self (OfficeViewSet): Instance of the OfficeViewSet class.
            request (Request): HTTP request object containing social media links update data.

        Returns:
            Response: Response indicating success or failure of the social
            media links update attempt.
        """
        success, message = OfficeService.office_update_social_links(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["PUT"],
        permission_classes=[],
        url_path="update-profile-image",
        url_name="update-profile-image",
    )
    @handle_service_exceptions
    def office_update_profile_image(self, request):
        """
        Updates office profile image.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the profile image update.
        """
        success, message = OfficeService.office_update_profile_image(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)
