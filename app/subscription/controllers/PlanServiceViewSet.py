"""
ViewSet module for the PlanService model.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.subscription.controllers.ManageSubscriptionPermission import ManageSubscriptionPermission
from app.subscription.models.PlanService import PlanService
from app.subscription.serializers.ServiceSerializer import ServiceSerializer


class PlanServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the PlanService model.
    """

    queryset = PlanService.objects.all()
    serializer_class = ServiceSerializer

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
            return [IsAuthenticated()]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), ManageSubscriptionPermission()]
        return super().get_permissions()
