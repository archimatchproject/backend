"""
Service module for the OfficeSubscriptionPlan model.

This module defines the service for handling the business logic and exceptions
related to OfficeSubscriptionPlan creation and management.

Classes:
    OfficeSubscriptionPlanService: Service class for OfficeSubscriptionPlan operations.
"""

from django.db import transaction

from app.subscription.models.OfficeSubscriptionPlan import OfficeSubscriptionPlan
from app.subscription.serializers.SubscriptionPlanSerializer import OfficeSubscriptionPlanSerializer
from app.users.models.Office import Office


class OfficeSubscriptionPlanService:
    """
    Service class for handling OfficeSubscriptionPlan operations.

    Handles business logic and exception handling for
    OfficeSubscriptionPlan creation and management.

    Methods:
        create_subscription_plan(data): Handles validation and creation
        of a new OfficeSubscriptionPlan.
        update_subscription_plan(subscription_plan_instance, data, partial=False): Handles
        updating an existing OfficeSubscriptionPlan.
        get_all_office_subscription_plans(): Retrieves all office subscription plans.
        office_get_upgradable_plans(request): Fetches upgradable plans for an office.
    """

    @classmethod
    def create_subscription_plan(cls, data):
        """
        Handles validation and creation of a new OfficeSubscriptionPlan.

        Args:
            data (dict): The validated data for creating an OfficeSubscriptionPlan instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = OfficeSubscriptionPlanSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        event_discount = validated_data.pop("event_discount_id", None)
        most_popular = validated_data.get("most_popular", False)

        with transaction.atomic():
            if most_popular:
                OfficeSubscriptionPlan.objects.filter(most_popular=True).update(most_popular=False)
            # Create OfficeSubscriptionPlan instance
            subscription_plan = OfficeSubscriptionPlan.objects.create(**validated_data, event_discount=event_discount)

            return True, OfficeSubscriptionPlanSerializer(subscription_plan).data

    @classmethod
    def update_subscription_plan(cls, instance, data, partial=False):
        """
        Handles the update of an existing OfficeSubscriptionPlan instance.

        Args:
            instance (OfficeSubscriptionPlan): The existing OfficeSubscriptionPlan instance.
            data (dict): The validated data for updating the OfficeSubscriptionPlan.
            partial (bool): Whether to perform partial update (default: False).

        Returns:
            Response: The response object containing the updated instance data.
        """

        serializer = OfficeSubscriptionPlanSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        event_discount = validated_data.pop("event_discount_id", None)
        most_popular = validated_data.get("most_popular", False)

        with transaction.atomic():
            if most_popular:
                OfficeSubscriptionPlan.objects.filter(most_popular=True).update(most_popular=False)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.event_discount = event_discount
            instance.clean()
            instance.save()

            return True, OfficeSubscriptionPlanSerializer(instance).data

    @classmethod
    def office_get_upgradable_plans(cls, request):
        """
        Handles fetching upgradable OfficeSubscriptionPlans for an office.

        Args:
            request (Request): The request object containing user data.

        Returns:
            Response: The response object containing the result of the operation.
        """

        user_id = request.user.id

        with transaction.atomic():
            office = Office.objects.get(user__id=user_id)
            current_plan = office.subscription_plan
            subscription_plans = OfficeSubscriptionPlan.objects.filter(plan_price__gt=current_plan.plan_price).order_by(
                "plan_price"
            )

            return True, OfficeSubscriptionPlanSerializer(subscription_plans, many=True).data

    @classmethod
    def get_all_office_subscription_plans(cls):
        """
        Retrieves all the office subscription plans.
        """
        subscription_plans = OfficeSubscriptionPlan.objects.all().order_by("plan_price")
        return True, OfficeSubscriptionPlanSerializer(subscription_plans, many=True).data
