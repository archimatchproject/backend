"""
Module: app.views.supplier

This module provides view classes for interacting with Supplier instances
using Django REST Framework, including custom actions for signup, login,
and profile management.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.users.controllers.SupplierFilter import SupplierFilter
from app.users.models.Supplier import Supplier
from app.users.serializers.SupplierSerializer import SupplierInputSerializer
from app.users.serializers.SupplierSerializer import SupplierSerializer
from app.users.serializers.UserAuthSerializer import UserAuthSerializer
from app.users.services.SupplierService import SupplierService
from rest_framework import status

class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet for interacting with Supplier instances.

    This ViewSet provides standard CRUD operations for Supplier instances,
    along with custom actions for signup, login, and profile management.
    """

    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = SupplierFilter

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="signup",
        serializer_class=UserAuthSerializer,
    )
    @handle_service_exceptions
    def supplier_signup(self, request):
        """
        Allows a supplier to sign up using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing signup data.

        Returns:
            Response: Response indicating success or failure of the signup attempt.
        """
        success,message = SupplierService.supplier_signup(request)
        return build_response(success=success, message=message, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="login",
        serializer_class=UserAuthSerializer,
    )
    def supplier_login(self, request):
        """
        Allows a supplier to login using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing login data.

        Returns:
            Response: Response indicating success or failure of the login attempt.
        """
        return SupplierService.supplier_login(request)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="first-connection",
        serializer_class=UserAuthSerializer,
    )
    def supplier_first_cnx(self, request):
        """
        Handles the first connection setup for a supplier using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing first connection data.

        Returns:
            Response: Response indicating success or failure of the first connection attempt.
        """
        return SupplierService.supplier_first_connection(request)

    @action(
        detail=False,
        methods=["PUT"],
        permission_classes=[],
        url_path="update-profile",
        serializer_class=SupplierInputSerializer,
    )
    def supplier_update_profile(self, request):
        """
        Allows a supplier to update their profile information using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing profile update data.

        Returns:
            Response: Response indicating success or failure of the profile update attempt.
        """
        return SupplierService.supplier_update_profile(request)

    @action(
        detail=False,
        methods=["PUT"],
        url_path="update-bio",
    )
    def supplier_update_bio(self, request):
        """
        Allows a supplier to update their bio settings using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing bio settings update data.

        Returns:
            Response: Response indicating success or failure of the bio settings update attempt.
        """
        return SupplierService.supplier_update_bio(request)

    @action(
        detail=False,
        methods=["PUT"],
        url_path="update-presentation-video",
    )
    def supplier_update_presentation_video(self, request):
        """
        Allows a supplier to update their bio settings using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing bio settings update data.

        Returns:
            Response: Response indicating success or failure of the bio settings update attempt.
        """
        return SupplierService.supplier_update_presentation_video(request)

    @action(
        detail=False,
        methods=["PUT"],
        permission_classes=[],
        url_path="update-links",
    )
    def supplier_update_links(self, request):
        """
        Allows a supplier to update their social media links using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing social media links update
             data.

        Returns:
            Response: Response indicating success or failure of the social media links
            update attempt.
        """
        return SupplierService.supplier_update_links(request)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="speciality-types",
    )
    def get_speciality_types(self, request):
        """
        Retrieves all speciality types.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing the speciality types.
        """
        return SupplierService.get_speciality_types()

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="appearances",
    )
    def get_appearances(self, request):
        """
        Retrieves all appearances.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing the appearances.
        """
        return SupplierService.get_appearances()

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="get-profile",
        url_name="get-profile",
    )
    def supplier_get_profile(self, request):
        """
        Retrieves supplier details.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing supplier details.
        """
        return SupplierService.supplier_get_profile(request)

    @action(
        detail=True,
        methods=["GET"],
        permission_classes=[],
        url_path="get-profile",
        url_name="get-profile-by-id",
    )
    def get_profile_by_id(self, request, pk=None):
        """
        Retrieves supplier details based on the provided ID.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object.
            pk (int): The primary key of the supplier.

        Returns:
            Response: Response containing supplier details.
        """
        return SupplierService.get_profile_by_id(pk)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="send-reset-password-link",
        url_name="send-reset-password-link",
    )
    def supplier_send_reset_password_link(self, request):
        """
        Retrieves supplier details.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing supplier details.
        """
        return SupplierService.supplier_send_reset_password_link(request)

    @action(
        detail=False,
        methods=["PUT"],
        url_path="update-profile-image",
    )
    def supplier_update_profile_image(self, request):
        """
        Allows a supplier to update their profile image using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing bio settings update data.

        Returns:
            Response: Response indicating success or failure of the bio settings update attempt.
        """
        return SupplierService.supplier_update_profile_image(request)

    @action(
        detail=False,
        methods=["PUT"],
        url_path="update-cover-image",
    )
    def supplier_update_cover_image(self, request):
        """
        Allows a supplier to update their cover image using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing bio settings update data.

        Returns:
            Response: Response indicating success or failure of the bio settings update attempt.
        """
        return SupplierService.supplier_update_cover_image(request)

    @action(
        detail=False,
        methods=["PUT"],
        url_path="update-visibility",
    )
    def supplier_update_visibility(self, request):
        """
        Allows a supplier to update their visibility using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing bio settings update data.

        Returns:
            Response: Response indicating success or failure of the bio settings update attempt.
        """
        return SupplierService.supplier_update_visibility(request)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="validate-password-token",
        url_name="validate-password-token",
    )
    def supplier_validate_password_token(self, request):
        """
        sends Supplier reset password email.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object.
        """
        return SupplierService.supplier_validate_password_token(request)

    def get(self, request):
        """
        Retrieve all suppliers.

        This method allows retrieval of all Supplier objects from the database.
        It delegates the actual retrieval to the `supplier_get_all` class method
        of `SupplierService`, which handles pagination and serialization.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP GET request object.

        Returns:
            Response: A paginated response containing serialized Supplier objects
                or an error response if there's a problem during retrieval.
        """
        return SupplierService.supplier_get_all(request)

    @action(
        detail=True,
        methods=["POST"],
        url_path="resend-email",
    )
    def supplier_resend_email(self, request, pk=None):
        """
        Custom action to resend email to supplier

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the supplier object

        Returns:
            Response: The response object containing the result of the operation.
        """
        return SupplierService.supplier_resend_email(pk)

    def delete(self, request, pk=None):
        """
        Deletes a supplier from the system.

        Args:
            request (Request): Django request object.
            pk (int): ID of the supplier to be deleted.

        Returns:
            Response: Response object indicating success or failure of the supplier deletion.
        """
        return SupplierService.delete_supplier(pk)

    @action(
        detail=False,
        methods=["PUT"],
        url_path="update-visibility",
    )
    def supplier_update_catalog_visibility(self, request):
        """
        Allows a supplier to update their visibility using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing bio settings update data.

        Returns:
            Response: Response indicating success or failure of the bio settings update attempt.
        """
        return SupplierService.supplier_update_catalog_visibility(request)

    @action(
        detail=False,
        methods=["DELETE"],
        url_path="delete-showroom",
    )
    def delete_showroom(self, request, pk=None):
        """
        deletes a showroom by id 
        Args:
            
            pk (int): The primary key of the showroom.

        Returns:
            Response: Response containing show room details.
        """
        return SupplierService.delete_showroom(pk)