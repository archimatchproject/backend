"""
Module: archimatch_views

This module contains view classes for interacting with ArchimatchUser instances
using Django REST Framework.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.serializers.ArchimatchUserObtainPairSerializer import (
    ArchimatchUserObtainPairSerializer,
)
from app.users.serializers.ArchimatchUserObtainPairSerializer import PhoneTokenObtainPairSerializer
from app.users.serializers.ArchimatchUserPWSerializer import ArchimatchUserCreatePWSerializer
from app.users.serializers.ArchimatchUserPWSerializer import ArchimatchUserResetPWSerializer
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSimpleSerializer
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

    def get_serializer_class(self):
        """
        Return the serializer class to be used for the request.
        """
        if self.action == "archimatch_user_create_password":
            return ArchimatchUserCreatePWSerializer
        elif self.action == "archimatch_user_reset_password":
            return ArchimatchUserResetPWSerializer
        elif self.action == "archimatch_user_update_data":
            return ArchimatchUserSimpleSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        """
        Override this method to specify custom permissions for different actions.
        """
        if self.action in ["archimatch_user_reset_password", "archimatch_user_update_data"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=False, methods=["POST"], url_path="create-password")
    def archimatch_user_create_password(self, request):
        """
        Action to create a password for an ArchimatchUser.

        Args:
            request (Request): HTTP request object containing user data.

        Returns:
            Response: HTTP response object indicating success or failure of password creation.
        """
        return ArchimatchUserService.archimatch_user_create_password(request)

    @action(detail=False, methods=["POST"], url_path="reset-password")
    def archimatch_user_reset_password(self, request):
        """
        Action to reset a password for an ArchimatchUser.

        Args:
            request (Request): HTTP request object containing user data.

        Returns:
            Response: HTTP response object indicating success or failure of password reset.
        """
        return ArchimatchUserService.archimatch_user_reset_password(request)

    @action(detail=False, methods=["PUT"], url_path="update-data")
    def archimatch_user_update_data(self, request):
        """
        Action to update data for an ArchimatchUser.

        Args:
            request (Request): HTTP request object containing user data.

        Returns:
            Response: HTTP response object indicating success or failure of updating data.
        """
        return ArchimatchUserService.archimatch_user_update_data(request)
