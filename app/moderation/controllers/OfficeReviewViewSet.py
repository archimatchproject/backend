"""
ViewSet module for the OfficeReview model.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
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
        if self.action in ["create", "architect_reviews"] or self.action in [
            "update",
            "partial_update",
            "destroy",
            "list",
            "retrieve",
        ]:
            return [IsAuthenticated()]
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

    @handle_service_exceptions
    def update(self, request, *args, **kwargs):
        """
        Override the update method to use OfficeReviewService for updating an existing review.

        Returns:
            Response: Response containing the updated review.
        """
        review = self.get_object()
        success, data = OfficeReviewService.update_office_review(request, review)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path="architect-reviews")
    @handle_service_exceptions
    def architect_reviews(self, request, pk=None):
        """
        Retrieve all reviews for a specific architect.

        Returns:
            Response: Serialized response containing the list of reviews.
        """
        success, data = OfficeReviewService.get_architect_reviews(pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path="architect-stats")
    @handle_service_exceptions
    def architect_stats(self, request, pk=None):
        """
        Retrieve statistical data about an architect’s office reviews.

        Returns:
            Response: JSON response containing rating counts and the dominant rating.
        """
        success, data = OfficeReviewService.get_architect_statistics(pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
