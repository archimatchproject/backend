"""
Module: app.views.supplier

This module provides view classes for interacting with Supplier instances
using Django REST Framework, including custom actions for signup, login,
and profile management.
"""

from rest_framework import viewsets
from rest_framework.decorators import action

from app.users.models.Supplier import Supplier
from app.users.serializers.SupplierSerializer import SupplierSerializer
from app.users.serializers.UserAuthSerializer import UserAuthSerializer
from app.users.services.SupplierService import SupplierService


class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet for interacting with Supplier instances.

    This ViewSet provides standard CRUD operations for Supplier instances,
    along with custom actions for signup, login, and profile management.
    """

    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="signup",
        serializer_class=UserAuthSerializer,
    )
    def supplier_signup(self, request):
        """
        Allows a supplier to sign up using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing signup data.

        Returns:
            Response: Response indicating success or failure of the signup attempt.
        """
        return SupplierService.supplier_signup(request)

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
