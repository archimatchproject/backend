"""
Module: app.views.client

This module provides view classes for interacting with Client instances
using Django REST Framework, including custom login actions.
"""

from rest_framework import viewsets
from rest_framework.decorators import action

from app.users.models.Client import Client
from app.users.serializers.ClientSerializer import ClientSerializer
from app.users.serializers.UserAuthSerializer import UserAuthPhoneSerializer
from app.users.serializers.UserAuthSerializer import UserAuthSerializer
from app.users.serializers.UserAuthSerializer import VerifyCodeSerializer
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
        url_path="send-code",
        serializer_class=UserAuthPhoneSerializer,
    )
    def client_send_verification_code(self, request):
        """
        Sends a verification code to the client's phone number.

        Args:
            request (Request): HTTP request object containing the phone number.

        Returns:
            Response: Response indicating whether the verification code was sent successfully.
        """
        return ClientService.client_send_verification_code(request)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="verify-code",
        serializer_class=VerifyCodeSerializer,
    )
    def client_verify_verification_code(self, request):
        """
        Verifies the client's phone number using the verification code.

        Args:
            request (Request): HTTP request object containing the phone number and
            verification code.

        Returns:
            Response: Response indicating success or failure of the verification.
        """
        return ClientService.client_verify_verification_code(request)
