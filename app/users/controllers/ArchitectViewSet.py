"""
Module: app.views.architectViewSet

Class: ArchitectViewSet

"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser

from app.users.models.Architect import Architect
from app.users.serializers.ArchitectSerializer import ArchitectSerializer
from app.users.services.ArchitectService import ArchitectService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

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

    def get_parser_classes(self):
        """
        Get the parsers that the view requires.
        """
        if self.action in ["architect_update_preferences"]:
            return JSONParser
        if self.action not in ["architect_update_base_details", "architect_update_company_details"]:
            return JSONParser
        else:
            return (JSONParser, MultiPartParser, FormParser)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="send-reset-password-link",
        url_name="send-reset-password-link",
    )
    @handle_service_exceptions
    def architect_send_reset_password_link(self, request):
        """
        Sends architect reset password email.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of sending the reset password link.
        """
        success,message = ArchitectService.architect_send_reset_password_link(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="validate-password-token",
        url_name="validate-password-token",
    )
    @handle_service_exceptions
    def architect_validate_password_token(self, request):
        """
        Validates the password reset token.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the token validation.
        """
        success,data = ArchitectService.architect_validate_password_token(request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="get-profile",
        url_name="get-profile",
    )
    @handle_service_exceptions
    def architect_get_profile(self, request):
        """
        Retrieves Architect details.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing Architect details.
        """
        success,architect_data = ArchitectService.architect_get_profile(request)
        return build_response(success=success, data=architect_data, status=status.HTTP_200_OK)


    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="update-base-details",
        url_name="update-base-details",
    )
    @handle_service_exceptions
    def architect_update_base_details(self, request):
        """
        Updates architect base information

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the base details update.
        """
        success,message = ArchitectService.architect_update_base_details(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)


    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="update-company-details",
        url_name="update-company-details",
    )
    @handle_service_exceptions
    def architect_update_company_details(self, request):
        """
        Updates architect company details.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the company details update.
        """
        success,message = ArchitectService.architect_update_company_details(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="update-needs",
        url_name="update-needs",
    )
    @handle_service_exceptions
    def architect_update_needs(self, request):
        """
        Updates architect needs.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the needs update.
        """
        success,message = ArchitectService.architect_update_needs(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["PUT"],
        permission_classes=[],
        url_path="update-preferences",
        url_name="update-preferences",
    )
    @handle_service_exceptions
    def architect_update_preferences(self, request):
        """
        Updates architect preferences.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the preferences update.
        """
        success,message = ArchitectService.architect_update_preferences(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["PUT"],
        permission_classes=[],
        url_path="update-profile-image",
        url_name="update-profile-image",
    )
    @handle_service_exceptions
    def architect_update_profile_image(self, request):
        """
        Updates architect profile image.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the profile image update.
        """
        success,message = ArchitectService.architect_update_profile_image(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)


    @action(
        detail=False,
        methods=["PUT"],
        permission_classes=[],
        url_path="update-presentation-video",
        url_name="update-presentation-video",
    )
    @handle_service_exceptions
    def architect_update_presentation_video(self, request):
        """
        Updates architect presentation video.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the presentation video update.
        """
        success,message = ArchitectService.architect_update_profile_image(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="wok-types",
        url_name="wok-types",
    )
    @handle_service_exceptions
    def get_architect_work_types(self, request):
        """
        Retrieves Architect details.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing Architect details.
        """
        success,data = ArchitectService.get_architect_work_types()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="property-types",
        url_name="property-types",
    )
    @handle_service_exceptions
    def get_property_types(self, request):
        """
        Retrieves Architect details.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing Architect details.
        """
        success,data = ArchitectService.get_property_types()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="terrain-surfaces",
        url_name="terrain-surfaces",
    )
    @handle_service_exceptions
    def get_terrain_surfaces(self, request):
        """
        Retrieves Architect details.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing Architect details.
        """
        success,data = ArchitectService.get_terrain_surfaces()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="work-surfaces",
        url_name="work-surfaces",
    )
    @handle_service_exceptions
    def get_work_surfaces(self, request):
        """
        Retrieves Architect details.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing Architect details.
        """
        success,data = ArchitectService.get_work_surfaces()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="budgets",
        url_name="budgets",
    )
    @handle_service_exceptions
    def get_budgets(self, request):
        """
        Retrieves Architect details.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing Architect details.
        """
        success,data = ArchitectService.get_budgets()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="locations",
        url_name="locations",
    )
    @handle_service_exceptions
    def get_locations(self, request):
        """
        Retrieves Architect details.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response containing Architect details.
        """
        success,data = ArchitectService.get_locations()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
    
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[],
        url_path="update-about",
        url_name="update-about",
    )
    @handle_service_exceptions
    def architect_update_about(self, request):
        """
        Updates architect about.

        Args:
            self (ArchitectViewSet): Instance of the ArchitectViewSet class.
            request (Request): HTTP request object.

        Returns:
            Response: Response object indicating the result of the needs update.
        """
        success,message = ArchitectService.architect_update_about(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

