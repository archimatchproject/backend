"""
REST API ViewSet for managing Blog instances.

This module defines a ViewSet for handling CRUD operations and additional actions
related to Blog instances via REST API endpoints.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.architect_realization.models.Realization import Realization
from app.architect_realization.serializers.RealizationSerializer import RealizationPOSTSerializer
from app.architect_realization.serializers.RealizationSerializer import RealizationSerializer
from app.architect_realization.services.RealizationService import RealizationService
from app.core.pagination import CustomPagination


class RealizationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling Blog instances.

    This ViewSet provides endpoints for CRUD operations and additional custom actions
    related to Blog instances. It includes default actions like list, create, retrieve,
    update, and destroy, as well as a custom action for retrieving all blogs.
    """

    queryset = Realization.objects.all()
    serializer_class = RealizationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        """
        Handle GET request and return paginated Realization objects.

        This method retrieves all Realization objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination is not applied correctly, it returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing Realization objects or an error message.
        """
        queryset = Realization.objects.all()

        # Instantiate the paginator
        paginator = self.pagination_class()
        print(paginator)

        # Apply pagination to the queryset
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = RealizationSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If pagination is not applied correctly, return a 400 Bad Request response
        serializer = RealizationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        url_path="create-realization",
        methods=["POST"],
        serializer_class=RealizationPOSTSerializer,
    )
    def realization_create(self, request):
        """
        Creating new realization
        """
        return RealizationService.realization_create(request)
