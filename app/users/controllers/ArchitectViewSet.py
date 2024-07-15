"""
Module: app.views.architectViewSet

Class: ArchitectViewSet

"""

from rest_framework import viewsets
from rest_framework.decorators import action

from app.users.models.Architect import Architect
from app.users.serializers.ArchitectSerializer import ArchitectSerializer
from app.users.services.ArchitectService import ArchitectService


class ArchitectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Architect model, providing CRUD operations and additional actions.

    Attributes:
        serializer_class: Serializer class for Architect model instances.
        queryset: Queryset containing all Architect instances.
        permission_classes: List of permission classes for this ViewSet.

    """

    serializer_class = ArchitectSerializer
    queryset = Architect.objects.all()

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="send-reset-password-link",
        url_name="send-reset-password-link",
    )
    def architect_send_reset_password_link(self, request):
        """
        sends architect reset password email.

        Args:
            self (architectViewSet): Instance of the architectViewSet class.
            request (Request): HTTP request object.
        """
        return ArchitectService.architect_send_reset_password_link(request)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="validate-password-token",
        url_name="validate-password-token",
    )
    def architect_validate_password_token(self, request):
        """
        sends architect reset password email.

        Args:
            self (architectViewSet): Instance of the architectViewSet class.
            request (Request): HTTP request object.
        """
        return ArchitectService.architect_validate_password_token(request)
