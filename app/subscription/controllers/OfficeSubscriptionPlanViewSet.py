"""
ViewSet module for the SubscriptionPlan model.

This module defines a ViewSet for handling CRUD operations and additional actions
related to SubscriptionPlan instances via REST API endpoints.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.subscription.controllers.ManageSubscriptionPermission import ManageSubscriptionPermission
from app.subscription.models.OfficeSubscriptionPlan import OfficeSubscriptionPlan
from app.subscription.serializers.SubscriptionPlanSerializer import OfficeSubscriptionPlanSerializer
from app.subscription.services.OfficeSubscriptionPlanService import OfficeSubscriptionPlanService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status


class OfficeSubscriptionPlanViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling OfficeSubscriptionPlan instances.

    This ViewSet provides endpoints for CRUD operations related to OfficeSubscriptionPlan instances.
    """

    queryset = OfficeSubscriptionPlan.objects.all()
    serializer_class = OfficeSubscriptionPlanSerializer

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
        Create a new OfficeSubscriptionPlan instance.

        Args:
            request (Request): The HTTP request object containing data to create
            OfficeSubscriptionPlan instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the created OfficeSubscriptionPlan instance.
        """
        success, data = OfficeSubscriptionPlanService.create_subscription_plan(request.data)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @handle_service_exceptions
    def update(self, request, *args, **kwargs):
        """
        Update an existing OfficeSubscriptionPlan instance.

        Args:
            request (Request): The HTTP request object containing data to update
            OfficeSubscriptionPlan instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the updated OfficeSubscriptionPlan instance.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        success, data = OfficeSubscriptionPlanService.update_subscription_plan(
            instance, request.data, partial=partial
        )
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="upgradable-plans", url_name="upgradable-plans")
    @handle_service_exceptions
    def get_upgradable_plans(self, request):
        """
        Custom action to fetch upgradable subscription plans for an office.

        Args:
            request (Request): The HTTP request object containing user data.

        Returns:
            Response: The response object containing the result of the operation.
        """
        success, data = OfficeSubscriptionPlanService.office_get_upgradable_plans(request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @handle_service_exceptions
    def list(self, request, *args, **kwargs):
        """
        List all OfficeSubscriptionPlan instances.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: Serialized data of all OfficeSubscriptionPlan instances.
        """
        success, data = OfficeSubscriptionPlanService.get_all_office_subscription_plans()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
