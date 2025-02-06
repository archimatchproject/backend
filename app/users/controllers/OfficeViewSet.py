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
from app.users.serializers.OfficeSerializer import OfficeSerializer
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
