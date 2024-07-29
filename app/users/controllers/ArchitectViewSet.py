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
        Sends architect reset password email.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of sending the reset password link.
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
        Validates the password reset token.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the token validation.
        """
        return ArchitectService.architect_validate_password_token(request)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="get-profile",
        url_name="get-profile",
    )
    def architect_get_profile(self, request):
        """
        Retrieves Architect details.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing Architect details.
        """
        return ArchitectService.architect_get_profile(request)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="update-base-details",
        url_name="update-base-details",
    )
    def architect_update_base_details(self, request):
        """
        Updates architect base information

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the base details update.
        """
        return ArchitectService.architect_update_base_information(request)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="update-company-details",
        url_name="update-company-details",
    )
    def architect_update_company_details(self, request):
        """
        Updates architect company details.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the company details update.
        """
        return ArchitectService.architect_update_company_details(request)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="update-needs",
        url_name="update-needs",
    )
    def architect_update_needs(self, request):
        """
        Updates architect needs.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the needs update.
        """
        return ArchitectService.architect_update_needs(request)
