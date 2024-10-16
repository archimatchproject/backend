"""
Service module for the SubscriptionPlan model.

This module defines the service for handling the business logic and exceptions
related to SubscriptionPlan creation and management.

Classes:
    SubscriptionPlanService: Service class for SubscriptionPlan operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.subscription.models.ArchitectSubscriptionPlan import ArchitectSubscriptionPlan
from app.subscription.models.SubscriptionPlan import SubscriptionPlan
from app.subscription.models.SupplierSubscriptionPlan import SupplierSubscriptionPlan
from app.subscription.serializers.SubscriptionPlanSerializer import ArchitectSubscriptionPlanSerializer, SubscriptionPlanSerializer, SupplierSubscriptionPlanSerializer
from app.users.models.Supplier import Supplier


class SupplierSubscriptionPlanService:
    """
    Service class for handling SubscriptionPlan operations.

    Handles business logic and exception handling for SubscriptionPlan creation and management.

    Methods:
        create_subscription_plan(data): Handles validation and creation of a new SubscriptionPlan.
        update_subscription_plan(subscription_plan_instance, data, partial=False): Handles
        updating an existing SubscriptionPlan.
    """

    @classmethod
    def create_subscription_plan(cls, data):
        """
        Handles validation and creation of a new SubscriptionPlan.

        Args:
            data (dict): The validated data for creating a SubscriptionPlan instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = SupplierSubscriptionPlanSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        event_discount = validated_data.pop("event_discount_id", None)
        most_popular = validated_data.get("most_popular", False)

        with transaction.atomic():
            if most_popular:
                SupplierSubscriptionPlan.objects.filter(most_popular=True).update(most_popular=False)
            # Create SubscriptionPlan instance
            subscription_plan = SupplierSubscriptionPlan.objects.create(**validated_data,event_discount=event_discount)

            return True,SupplierSubscriptionPlanSerializer(subscription_plan).data
        
    @classmethod
    def update_subscription_plan(cls, instance, data, partial=False):
        """
        Handle the update of an existing SubscriptionPlan instance along with related
        PlanService instances.

        Args:
            instance (SubscriptionPlan): The existing SubscriptionPlan instance.
            data (dict): The validated data for updating a SubscriptionPlan.
            partial (bool): Whether to perform partial update (default: False).

        Returns:
            Response: The response object containing the updated instance data.
        """

        serializer = SupplierSubscriptionPlanSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        event_discount = validated_data.pop("event_discount_id",None)
        most_popular = validated_data.get("most_popular", False)

        with transaction.atomic():
            if most_popular:
                ArchitectSubscriptionPlan.objects.filter(most_popular=True).update(most_popular=False)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.event_discount = event_discount
            instance.clean()
            instance.save()

            return True,SupplierSubscriptionPlanSerializer(instance).data
        
    @classmethod
    def supplier_get_upgradable_plans(cls, request):
        """
        Handles fetching upgradable SubscriptionPlans for an architect.

        Args:
            request (Request): The request object containing user data.

        Returns:
            Response: The response object containing the result of the operation.
        """

        user_id = request.user.id

        with transaction.atomic():
            supplier = Supplier.objects.get(user__id=user_id)
            current_plan = supplier.subscription_plan
            subscription_plans = SupplierSubscriptionPlan.objects.filter(
                plan_price__gt=current_plan.plan_price
            ).order_by("plan_price")

            return True,SupplierSubscriptionPlanSerializer(subscription_plans, many=True).data
        
    @classmethod
    def get_all_supplier_subscription_plan(cls):
        """
        gets all the supplier subscription plans
        """
        subscription_plans = SupplierSubscriptionPlan.objects.all().order_by("plan_price")
        return True,SupplierSubscriptionPlanSerializer(subscription_plans,many=True).data