"""
Module: app.views.admin

Class: AdminViewSet

"""

from rest_framework import viewsets
from rest_framework.decorators import action

from app.users.controllers.utils.IsSuperUser import IsSuperUser
from app.users.models.Admin import Admin
from app.users.serializers.AdminSerializer import AdminSerializer
from app.users.serializers.UserAuthSerializer import UserAuthSerializer
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
    permission_classes = [IsSuperUser]

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

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        name="retrieve_by_token",
    )
    def retrieve_by_token(self, request):
        """
        Retrieve admin details using a token provided in the request.

        Args:
            self: Instance of the AdminViewSet class.
            request: HTTP request object containing token.

        Returns:
            Response: Response containing admin details retrieved using the token.
        """
        return AdminService.retrieve_by_token(request)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        name="login",
        serializer_class=UserAuthSerializer,
    )
    def login(self, request):
        """
        Log in an admin using credentials provided in the request.

        Args:
            self: Instance of the AdminViewSet class.
            request: HTTP request object containing login credentials.

        Returns:
            Response: Response indicating success or failure of admin login.
        """
        return AdminService.admin_login(request)
