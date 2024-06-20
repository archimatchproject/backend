"""
Module: app.views.client

This module provides view classes for interacting with Client instances
using Django REST Framework, including custom login actions.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.users.models import Client
from app.users.serializers import (
    ClientSerializer,
    UserAuthPhoneSerializer,
    UserAuthSerializer,
)
from app.users.services import ClientService


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
        name="login",
        serializer_class=UserAuthSerializer,
    )
    def login_email(self, request):
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
        name="login",
        serializer_class=UserAuthPhoneSerializer,
    )
    def login_phone(self, request):
        """
        Performs phone number-based login for clients using a custom action.

        Args:
            self (ClientViewSet): Instance of the ClientViewSet class.
            request (Request): HTTP request object containing login data.

        Returns:
            Response: Response indicating success or failure of the login attempt.
        """
        return ClientService.client_login_phone(request)
