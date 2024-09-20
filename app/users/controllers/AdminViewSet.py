"""
Module: app.views.admin

Class: AdminViewSet

"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.users.controllers.utils.IsSuperUser import IsSuperUser
from app.users.models.Admin import Admin
from app.users.serializers.AdminSerializer import AdminSerializer
from app.users.services.AdminService import AdminService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

class AdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Admin model, providing CRUD operations and additional actions.

    Attributes:
        serializer_class: Serializer class for Admin model instances.
        queryset: Queryset containing all Admin instances.
        permission_classes: List of permission classes for this ViewSet.

    """

    serializer_class = AdminSerializer
    queryset = Admin.objects.all()

    def get_permissions(self):
        """
        Override this method to specify custom permissions for different actions.
        """
        if self.action in ["create", "update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsSuperUser]
        elif self.action in ["admin_send_reset_password_link", "admin_validate_password_token"]:
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Create a new admin based on the request data.

        Args:
            self: Instance of the AdminViewSet class.
            request: HTTP request object containing admin data.

        Returns:
            Response: Response indicating success or failure of admin creation.
        """
        success,admin_data = AdminService.create_admin(request)
        return build_response(success=success, data=admin_data, status=status.HTTP_201_CREATED)
        

    @handle_service_exceptions
    def update(self, request, *args, **kwargs):
        """
        Update an existing admin instance.

        Args:
            self: Instance of the AdminViewSet class.
            request: HTTP request object containing updated admin data.

        Returns:
            Response: Response indicating success or failure of admin update.
        """
        instance = self.get_object()
        success,admin_data = AdminService.update_admin(instance, request.data)
        return build_response(success=success, data=admin_data, status=status.HTTP_200_OK)


    @action(detail=False, methods=["GET"], url_path="get-permissions", name="get_permissions")
    @handle_service_exceptions
    def get_admin_permissions(self, request):
        """
        Get all permissions with their associated colors.

        Args:
            self: Instance of the AdminViewSet class.
            request: HTTP request object.

        Returns:
            Response: Response containing all permissions and their colors.
        """
        success,permissions_data = AdminService.get_all_permissions()
        return build_response(success=success, data=permissions_data, status=status.HTTP_200_OK) 

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="send-reset-password-link",
        url_name="send-reset-password-link",
    )
    @handle_service_exceptions
    def admin_send_reset_password_link(self, request):
        """
        sends admin reset password email.

        Args:
            self (adminViewSet): Instance of the adminViewSet class.
            request (Request): HTTP request object.
        """
        success,message = AdminService.admin_send_reset_password_link(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK) 
        
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="validate-password-token",
        url_name="validate-password-token",
    )
    @handle_service_exceptions
    def admin_validate_password_token(self, request):
        """
        sends admin reset password email.

        Args:
            self (adminViewSet): Instance of the adminViewSet class.
            request (Request): HTTP request object.
        """
        success,admin_data = AdminService.admin_validate_password_token(request)
        return build_response(success=success, data=admin_data, status=status.HTTP_200_OK) 
