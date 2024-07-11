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
from rest_framework.response import Response

from app.subscription.models.SubscriptionPlan import SubscriptionPlan
from app.subscription.serializers.SubscriptionPlanSerializer import SubscriptionPlanSerializer


class SubscriptionPlanService:
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
        serializer = SubscriptionPlanSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        plan_services = validated_data.pop("plan_services", [])

        try:
            with transaction.atomic():
                # Create SubscriptionPlan instance
                subscription_plan = SubscriptionPlan.objects.create(**validated_data)
                subscription_plan.services.set(plan_services)

                return Response(
                    SubscriptionPlanSerializer(subscription_plan).data,
                    status=status.HTTP_201_CREATED,
                )
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating subscription plan: {str(e)}")

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
        serializer = SubscriptionPlanSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        plan_services = validated_data.pop("plan_services", [])

        try:
            with transaction.atomic():
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                instance.services.set(plan_services)

                return Response(
                    SubscriptionPlanSerializer(instance).data, status=status.HTTP_200_OK
                )
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating subscription plan: {str(e)}")
