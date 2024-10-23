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
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

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

    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Override the create method to use ClientReviewService for handling the creation
        of a ProjectReport.
        """
        success,data = ClientReviewService.create_client_review(request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @action(detail=True, methods=["GET"], url_path="architect-reviews")
    @handle_service_exceptions
    def architect_reviews(self, request):
        """
        Retrieve all reviews for a specific architect.

        Args:
            pk (str): The primary key of the architect.

        Returns:
            Response: A serialized response containing the list of reviews.
        """
        success,data = ClientReviewService.get_architect_reviews(request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

