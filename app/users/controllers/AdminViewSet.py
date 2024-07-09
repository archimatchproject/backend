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
        if self.action in ["create", "update"]:
            self.permission_classes = [IsAuthenticated, IsSuperUser]
        if self.action in ["list"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Create a new admin based on the request data.

        Args:
            self: Instance of the AdminViewSet class.
            request: HTTP request object containing admin data.

        Returns:
            Response: Response indicating success or failure of admin creation.
        """
        return AdminService.create_admin(request.data)

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
        return AdminService.update_admin(instance, request.data)

    @action(detail=False, methods=["GET"], url_path="get-permissions", name="get_permissions")
    def get_admin_permissions(self, request):
        """
        Get all permissions with their associated colors.

        Args:
            self: Instance of the AdminViewSet class.
            request: HTTP request object.

        Returns:
            Response: Response containing all permissions and their colors.
        """
        return AdminService.get_all_permissions()
