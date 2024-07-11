"""
ViewSet module for the TokenPack model.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.subscription.controllers.ManageSubscriptionPermission import ManageSubscriptionPermission
from app.subscription.models.TokenPack import TokenPack
from app.subscription.serializers.TokenPackSerializer import TokenPackSerializer


class TokenPackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the TokenPack model.
    """

    queryset = TokenPack.objects.all()
    serializer_class = TokenPackSerializer

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
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), ManageSubscriptionPermission()]
        return super().get_permissions()
