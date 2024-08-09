"""
ViewSet module for the ClientReview model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.moderation.controllers.ManageReportingPermission import ManageReportingPermission
from app.moderation.models.ClientReview import ClientReview
from app.moderation.serializers.ClientReviewSerializer import ClientReviewSerializer
from app.moderation.services.ClientReviewService import ClientReviewService


class ClientReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ClientReview model.
    """

    queryset = ClientReview.objects.all()
    serializer_class = ClientReviewSerializer

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["create", "architect_reviews"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy", "list", "retrieve"]:
            return [IsAuthenticated(), ManageReportingPermission()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Override the create method to use ClientReviewService for handling the creation
        of a ProjectReport.
        """
        return ClientReviewService.create_client_review(request)

    @action(detail=True, methods=["GET"], url_path="architect-reviews")
    def architect_reviews(self, request):
        """
        Retrieve all reviews for a specific architect.

        Args:
            pk (str): The primary key of the architect.

        Returns:
            Response: A serialized response containing the list of reviews.
        """
        return ClientReviewService.get_architect_reviews(request)
