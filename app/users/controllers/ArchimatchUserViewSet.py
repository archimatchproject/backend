"""
Module: archimatch_views

This module contains view classes for interacting with ArchimatchUser instances
using Django REST Framework.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework_simplejwt.views import TokenObtainPairView

from app.users.models import ArchimatchUser
from app.users.serializers.ArchimatchUserCreatePWSerializer import ArchimatchUserCreatePWSerializer
from app.users.serializers.ArchimatchUserObtainPairSerializer import (
    ArchimatchUserObtainPairSerializer,
)
from app.users.serializers.ArchimatchUserObtainPairSerializer import PhoneTokenObtainPairSerializer
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer
from app.users.services.ArchimatchUserService import ArchimatchUserService


class ArchimatchUserObtainPairView(TokenObtainPairView):
    """
    View for obtaining JSON Web Tokens for ArchimatchUser.

    Inherits from TokenObtainPairView and uses ArchimatchUserObtainPairSerializer
    for token retrieval.
    """

    serializer_class = ArchimatchUserObtainPairSerializer


class PhoneTokenObtainPairView(TokenObtainPairView):
    """
    View for obtaining JSON Web Tokens for ArchimatchUser.

    Inherits from TokenObtainPairView and uses PhoneTokenObtainPairSerializer
    for token retrieval.
    """

    serializer_class = PhoneTokenObtainPairSerializer


class ArchimatchUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for interacting with ArchimatchUser instances.

    This ViewSet restricts all operations to disallow direct interaction with
    ArchimatchUser instances, raising MethodNotAllowed for all standard CRUD methods.
    """

    queryset = ArchimatchUser.objects.all()
    serializer_class = ArchimatchUserSerializer

    def list(self, request, *args, **kwargs):
        """
        MethodNotAllowed exception for listing ArchimatchUser instances.

        Raises:
            MethodNotAllowed: Always raised to disallow GET requests.
        """
        raise MethodNotAllowed("GET")

    def retrieve(self, request, *args, **kwargs):
        """
        MethodNotAllowed exception for retrieving a single ArchimatchUser instance.

        Raises:
            MethodNotAllowed: Always raised to disallow GET requests.
        """
        raise MethodNotAllowed("GET")

    def create(self, request, *args, **kwargs):
        """
        MethodNotAllowed exception for creating a new ArchimatchUser instance.

        Raises:
            MethodNotAllowed: Always raised to disallow POST requests.
        """
        raise MethodNotAllowed("POST")

    def update(self, request, *args, **kwargs):
        """
        MethodNotAllowed exception for updating an existing ArchimatchUser instance.

        Raises:
            MethodNotAllowed: Always raised to disallow PUT requests.
        """
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        """
        MethodNotAllowed exception for partially updating an ArchimatchUser instance.

        Raises:
            MethodNotAllowed: Always raised to disallow PATCH requests.
        """
        raise MethodNotAllowed("PATCH")

    def destroy(self, request, *args, **kwargs):
        """
        MethodNotAllowed exception for deleting an ArchimatchUser instance.

        Raises:
            MethodNotAllowed: Always raised to disallow DELETE requests.
        """
        raise MethodNotAllowed("DELETE")

    @action(
        detail=False,
        methods=["POST"],
        url_path="create-password",
        serializer_class=ArchimatchUserCreatePWSerializer,
    )
    def archimatch_user_create_password(self, request):
        """
        Action to create a password for an ArchimatchUser.

        Args:
            request (Request): HTTP request object containing user data.

        Returns:
            Response: HTTP response object indicating success or failure of password creation.
        """
        return ArchimatchUserService.archimatch_user_create_password(request)

    @action(
        detail=False,
        methods=["POST"],
        url_path="reset-password",
    )
    def archimatch_user_reset_password(self, request):
        """
        Action to reset a password for an ArchimatchUser.

        Args:
            request (Request): HTTP request object containing user data.

        Returns:
            Response: HTTP response object indicating success or failure of password reset.
        """
        return ArchimatchUserService.archimatch_user_reset_password(request)
