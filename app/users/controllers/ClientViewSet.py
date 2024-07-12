"""
Module: app.views.client

This module provides view classes for interacting with Client instances
using Django REST Framework, including custom login actions.
"""

from rest_framework import viewsets
from rest_framework.decorators import action

from app.users.models.Client import Client
from app.users.serializers.ClientSerializer import ClientSerializer
from app.users.serializers.UserAuthSerializer import UserAuthSerializer
from app.users.services.ClientService import ClientService


class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for interacting with Client instances.

    This ViewSet provides standard CRUD operations for Client instances,
    along with custom actions for email-based and phone-based logins.
    """

    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="login-email",
        serializer_class=UserAuthSerializer,
    )
    def client_login_email(self, request):
        """
        Performs email-based login for clients using a custom action.

        Args:
            self (ClientViewSet): Instance of the ClientViewSet class.
            request (Request): HTTP request object containing login data.

        Returns:
            Response: Response indicating success or failure of the login attempt.
        """
        return ClientService.client_login_email(request)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="send-reset-password-link",
        url_name="send-reset-password-link",
    )
    def client_send_reset_password_link(self, request):
        """
        sends client reset password email.

        Args:
            self (ClientViewSet): Instance of the ClientViewSet class.
            request (Request): HTTP request object.
        """
        return ClientService.client_send_reset_password_link(request)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="validate-password-token",
        url_name="validate-password-token",
    )
    def client_validate_password_token(self, request):
        """
        sends client reset password email.

        Args:
            self (ClientViewSet): Instance of the ClientViewSet class.
            request (Request): HTTP request object.
        """
        return ClientService.client_validate_password_token(request)
