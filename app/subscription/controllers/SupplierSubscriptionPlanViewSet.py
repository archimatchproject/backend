"""
ViewSet module for the SubscriptionPlan model.

This module defines a ViewSet for handling CRUD operations and additional actions
related to SubscriptionPlan instances via REST API endpoints.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.subscription.controllers.ManageSubscriptionPermission import ManageSubscriptionPermission
from app.subscription.models.SupplierSubscriptionPlan import SupplierSubscriptionPlan
from app.subscription.serializers.SubscriptionPlanSerializer import SupplierSubscriptionPlanSerializer
from app.subscription.services.SupplierSubscriptionPlanService import SupplierSubscriptionPlanService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

class SupplierSubscriptionPlanViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling SubscriptionPlan instances.

    This ViewSet provides endpoints for CRUD operations related to SubscriptionPlan instances.
    """

    queryset = SupplierSubscriptionPlan.objects.all()
    serializer_class = SupplierSubscriptionPlanSerializer

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

    @handle_service_exceptions
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
        success,data = SupplierSubscriptionPlanService.create_subscription_plan(request.data)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @handle_service_exceptions
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
        success,data = SupplierSubscriptionPlanService.update_subscription_plan(
            instance, request.data, partial=partial
        )
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @action(detail=False, methods=["get"], url_path="upgradable-plans", url_name="upgradable-plans")
    @handle_service_exceptions
    def get_upgradable_plans(self, request):
        """
        Custom action to fetch upgradable subscription plans for an architect.

        Args:
            request (Request): The HTTP request object containing user data.

        Returns:
            Response: The response object containing the result of the operation.
        """
        success,data = SupplierSubscriptionPlanService.supplier_get_upgradable_plans(request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
