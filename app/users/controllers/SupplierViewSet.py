"""
Module: app.views.supplier

This module provides view classes for interacting with Supplier instances
using Django REST Framework, including custom actions for signup, login,
and profile management.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.users.models import Supplier
from app.users.serializers import SupplierSerializer, UserAuthSerializer
from app.users.services import SupplierService


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
        name="signup",
        serializer_class=UserAuthSerializer,
    )
    def signup(self, request):
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
        name="login",
        serializer_class=UserAuthSerializer,
    )
    def login(self, request):
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
        name="first_connection",
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
        methods=["POST"],
        permission_classes=[],
        name="update_profile",
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
        methods=["POST"],
        permission_classes=[],
        name="update_general_settings",
    )
    def supplier_update_general_settings(self, request):
        """
        Allows a supplier to update their general settings using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing general settings update data.

        Returns:
            Response: Response indicating success or failure of the general settings update attempt.
        """
        return SupplierService.supplier_update_general_settings(request)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        name="update_links",
    )
    def supplier_update_links(self, request):
        """
        Allows a supplier to update their social media links using a custom action.

        Args:
            self (SupplierViewSet): Instance of the SupplierViewSet class.
            request (Request): HTTP request object containing social media links update data.

        Returns:
            Response: Response indicating success or failure of the social media links update attempt.
        """
        return SupplierService.supplier_update_links(request)
