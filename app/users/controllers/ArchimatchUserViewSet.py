"""
Module: archimatch_views

This module contains view classes for interacting with ArchimatchUser instances
using Django REST Framework.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from app.users.controllers.NotDeletedPermission import NotDeletedPermission
from app.users.controllers.NotSuspendedPermission import NotSuspendedPermission
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.serializers.ArchimatchUserObtainPairSerializer import (
    ArchimatchUserObtainPairSerializer,
)
from app.users.serializers.ArchimatchUserObtainPairSerializer import PhoneTokenObtainPairSerializer
from app.users.serializers.ArchimatchUserPWSerializer import ArchimatchUserCreatePWSerializer
from app.users.serializers.ArchimatchUserPWSerializer import ArchimatchUserResetPWSerializer
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSimpleSerializer
from app.users.serializers.UserAuthSerializer import UserAuthPhoneSerializer
from app.users.serializers.UserAuthSerializer import VerifyCodeSerializer
from app.users.services.ArchimatchUserService import ArchimatchUserService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

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
        elif self.action == "archimatch_user_get_user_data":
            return ArchimatchUserSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        """
        Override this method to specify custom permissions for different actions.
        """
        if self.action in [
            "archimatch_user_reset_password",
            "archimatch_user_update_data",
            "archimatch_user_get_user_data",
        ]:
            self.permission_classes = [
                IsAuthenticated,
                NotDeletedPermission,
                NotSuspendedPermission,
            ]
        return super().get_permissions()

    @action(detail=False, methods=["POST"], url_path="create-password")
    @handle_service_exceptions
    def archimatch_user_create_password(self, request):
        """
        Action to create a password for an ArchimatchUser.

        Args:
            request (Request): HTTP request object containing user data.

        Returns:
            Response: HTTP response object indicating success or failure of password creation.
        """
        success,token,message = ArchimatchUserService.archimatch_user_create_password(request)
        return build_response(success=success,message=message ,data=token, status=status.HTTP_200_OK)


    @action(detail=False, methods=["POST"], url_path="reset-password")
    @handle_service_exceptions
    def archimatch_user_reset_password(self, request):
        """
        Action to reset a password for an ArchimatchUser.

        Args:
            request (Request): HTTP request object containing user data.

        Returns:
            Response: HTTP response object indicating success or failure of password reset.
        """
        success,message = ArchimatchUserService.archimatch_user_reset_password(request)
        return build_response(success=success,message=message, status=status.HTTP_200_OK)


    @action(detail=False, methods=["PUT"], url_path="update-data")
    @handle_service_exceptions
    def archimatch_user_update_data(self, request):
        """
        Action to update data for an ArchimatchUser.

        Args:
            request (Request): HTTP request object containing user data.

        Returns:
            Response: HTTP response object indicating success or failure of updating data.
        """
        success,user_data,message = ArchimatchUserService.archimatch_user_update_data(request)
        return build_response(success=success,message=message ,data=user_data, status=status.HTTP_200_OK)

        

    @action(detail=False, methods=["GET"], url_path="get-user-data")
    @handle_service_exceptions
    def archimatch_user_get_user_data(self, request):
        """
        Action to get data for the authenticated ArchimatchUser.

        Args:
            request (Request): HTTP request object containing user data.

        Returns:
            Response: HTTP response object with the user data.
        """
        success,data = ArchimatchUserService.archimatch_user_get_user_data(request)
        return build_response(success=success,data=data, status=status.HTTP_200_OK)
        

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="send-code",
        serializer_class=UserAuthPhoneSerializer,
    )
    @handle_service_exceptions
    def send_verification_code(self, request):
        """
        Sends a verification code to the client's phone number.

        Args:
            request (Request): HTTP request object containing the phone number.

        Returns:
            Response: Response indicating whether the verification code was sent successfully.
        """
        success,message = ArchimatchUserService.send_verification_code(request)
        return build_response(success=success,message=message, status=status.HTTP_200_OK)


    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="verify-code",
        serializer_class=VerifyCodeSerializer,
    )
    @handle_service_exceptions
    def verify_verification_code(self, request):
        """
        Verifies the client's phone number using the verification code.

        Args:
            request (Request): HTTP request object containing the phone number and
            verification code.

        Returns:
            Response: Response indicating success or failure of the verification.
        """
        success,message = ArchimatchUserService.verify_verification_code(request)
        return build_response(success=success,message=message, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="verify-credentials",
    )
    @handle_service_exceptions
    def archimatch_user_is_found(self, request):
        """
        Verifies the client's phone number using the verification code.

        Args:
            request (Request): HTTP request object containing the phone number and
            verification code.

        Returns:
            Response: Response indicating success or failure of the verification.
        """
        success,message = ArchimatchUserService.archimatch_user_is_found(request)
        return build_response(success=success,message=message, status=status.HTTP_200_OK)

