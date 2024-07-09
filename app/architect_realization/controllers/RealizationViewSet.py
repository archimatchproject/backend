"""
REST API ViewSet for managing Blog instances.

This module defines a ViewSet for handling CRUD operations and additional actions
related to Blog instances via REST API endpoints.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.architect_realization.models.Realization import Realization
from app.architect_realization.serializers.RealizationSerializer import RealizationPOSTSerializer
from app.architect_realization.serializers.RealizationSerializer import RealizationSerializer
from app.architect_realization.services.RealizationService import RealizationService


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
