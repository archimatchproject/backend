"""
ViewSet module for the OfficeReview model.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.moderation.controllers.ManageReportingPermission import ManageReportingPermission
from app.moderation.models import OfficeReview
from app.moderation.serializers import OfficeReviewSerializer
from app.moderation.services.OfficeReviewService import OfficeReviewService


class OfficeReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the OfficeReview model.
    """

    queryset = OfficeReview.objects.all()
    serializer_class = OfficeReviewSerializer

    def get_permissions(self):
        """
        Get the permissions required for each action.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["create", "architect_reviews"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy", "list", "retrieve"]:
            return [IsAuthenticated(), ManageReportingPermission()]
        return super().get_permissions()

    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Override the create method to use OfficeReviewService for handling creation.

        Returns:
            Response: Response containing the newly created review.
        """
        success, data = OfficeReviewService.create_office_review(request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path="architect-reviews")
    @handle_service_exceptions
    def architect_reviews(self, request):
        """
        Retrieve all reviews for a specific architect.

        Returns:
            Response: Serialized response containing the list of reviews.
        """
        success, data = OfficeReviewService.get_architect_reviews(request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path="architect-stats")
    @handle_service_exceptions
    def architect_stats(self, request):
        """
        Retrieve statistical data about an architect’s office reviews.

        Returns:
            Response: JSON response containing rating counts and the dominant rating.
        """
        success, data = OfficeReviewService.get_architect_statistics(request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
