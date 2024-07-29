"""
ViewSet module for the Collection model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.catalogue.models.Collection import Collection
from app.catalogue.serializers.CollectionSerializer import CollectionSerializer
from app.catalogue.services.CollectionService import CollectionService


class CollectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Collection model.
    """

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        For `list` and `retrieve` actions (`GET` requests), no specific permissions are required.
        For `create`, `update`, `partial_update`, and `destroy` actions
        (`POST`, `PUT`, `PATCH`, `DELETE` requests),
        the view requires `IsAuthenticated` permissions.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["list", "retrieve"]:
            return []
        elif self.action in ["create", "update", "partial_update", "destroy", "update_order"]:
            return [
                IsAuthenticated(),
            ]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Override the create method to use CollectionService for handling the creation
         of a Collection.
        """
        return CollectionService.create_collection(request, request.data)

    @action(detail=True, methods=["PUT"])
    def update_order(self, request, pk=None):
        """
        Update the order of products within a collection.

        Args:
            request (Request): The request object containing the list of product ids
              in the new order.
            pk (int): The primary key of the collection.

        Returns:
            Response: The response object containing the result of the operation.
        """

        return CollectionService.update_product_order(request, pk, request.data)
