from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.officeOffer.models import Offer
from app.officeOffer.serializers import (
    OfferPOSTSerializer, OfferOutputSerializer, OfferPUTSerializer)
from app.officeOffer.services.OfferService import OfferService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.officeOffer.serializers.TechnicalSkillSerializer import TechnicalSkillSerializer
from app.officeOffer.serializers.SoftwareSkillSerializer import SoftwareSkillSerializer


class OfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Offer model.
    
    Provides endpoints for viewing, creating, updating, and retrieving job offers.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferOutputSerializer

    def get_permissions(self):
        """
        Apply different permissions based on the action being executed.
        Returns:
            list: The list of permission classes.
        """
        if self.action in [
            "update_offer",
            "list_offers",
            "offer_details",
        ]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []
        return super().get_permissions()

    def get_queryset(self):
        """
        Filter offers based on the office of the authenticated user.
        """
        user = self.request.user
        return Offer.objects.filter(office__user=user)

    @action(
            detail=False, 
            methods=["POST"], 
            url_path="create-offer", 
            serializer_class=OfferPOSTSerializer)
    @handle_service_exceptions
    def create_offer(self, request):
        """
        Create a new job offer.
        """
        success, data, message = OfferService.create_offer(request)
        return build_response(
            success=success, 
            data=data, message=message, status=status.HTTP_201_CREATED)

    @action(
            detail=True, 
            methods=["PUT"], url_path="update-offer", serializer_class=OfferPUTSerializer)
    @handle_service_exceptions
    def update_offer(self, request, pk=None):
        """
        Update an existing job offer.
        """
        instance = Offer.objects.get(id=pk)
        success, data, message = OfferService.update_offer(instance=instance, data=request.data)
        return build_response(
            success=success, 
            data=data, message=message, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="list-offers")
    @handle_service_exceptions
    def list_offers(self, request):
        """
        Retrieve and return paginated job offers.
        """
        return OfferService.get_offers(request)

    @action(detail=True, methods=["GET"], url_path="offer-details")
    @handle_service_exceptions
    def offer_details(self, request, pk=None):
        """
        Retrieve details of a specific job offer.
        """
        success, data = OfferService.get_offer_details(request, pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="contract-types")
    def get_contract_types(self, request):
        """
        Retrieve predefined contract types.
        """
        success, data = OfferService.get_contract_types()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="contract-durations")
    def get_contract_durations(self, request):
        """
        Retrieve predefined contract durations.
        """
        success, data = OfferService.get_contract_durations()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="work-locations")
    def get_work_locations(self, request):
        """
        Retrieve predefined work locations.
        """
        success, data = OfferService.get_work_locations()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="salary-ranges")
    def get_salary_ranges(self, request):
        """
        Retrieve predefined salary ranges.
        """
        success, data = OfferService.get_salary_ranges()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="experience-levels")
    def get_experience_levels(self, request):
        """
        Retrieve predefined experience levels.
        """
        success, data = OfferService.get_experience_levels()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="technical-skills",
        url_name="technical-skills",
        serializer_class=TechnicalSkillSerializer,
    )
    @handle_service_exceptions
    def get_technical_skills(self, request):
        """
        Retrieves all technical skills.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of technical skills.
        """
        success, data = OfferService.get_technical_skills()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[],
        url_path="software-skills",
        url_name="software-skills",
        serializer_class=SoftwareSkillSerializer,
    )
    @handle_service_exceptions
    def get_software_skills(self, request):
        """
        Retrieves all software skills.

        Args:
            request (Request): HTTP request object.

        Returns:
            Response: Response containing list of software skills.
        """
        success, data = OfferService.get_software_skills()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
