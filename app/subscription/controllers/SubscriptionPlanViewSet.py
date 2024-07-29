"""
ViewSet module for the SubscriptionPlan model.

This module defines a ViewSet for handling CRUD operations and additional actions
related to SubscriptionPlan instances via REST API endpoints.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.subscription.controllers.ManageSubscriptionPermission import ManageSubscriptionPermission
from app.subscription.models.SubscriptionPlan import SubscriptionPlan
from app.subscription.serializers.SubscriptionPlanSerializer import SubscriptionPlanSerializer
from app.subscription.services.SubscriptionPlanService import SubscriptionPlanService


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling SubscriptionPlan instances.

    This ViewSet provides endpoints for CRUD operations related to SubscriptionPlan instances.
    """

    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

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

    def create(self, request, *args, **kwargs):
        """
        Create a new SubscriptionPlan instance.

        Args:
            request (Request): The HTTP request object containing data to create
            SubscriptionPlan instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the created SubscriptionPlan instance.
        """
        return SubscriptionPlanService.create_subscription_plan(request.data)

    def update(self, request, *args, **kwargs):
        """
        Update an existing SubscriptionPlan instance.

        Args:
            request (Request): The HTTP request object containing data to update
            SubscriptionPlan instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the updated SubscriptionPlan instance.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        return SubscriptionPlanService.update_subscription_plan(
            instance, request.data, partial=partial
        )
