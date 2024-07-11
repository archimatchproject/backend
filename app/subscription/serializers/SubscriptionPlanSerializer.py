"""
Serializer module for the SubscriptionPlan model.
"""

from rest_framework import serializers

from app.subscription.models.PlanService import PlanService
from app.subscription.models.SubscriptionPlan import SubscriptionPlan
from app.subscription.serializers.ServiceSerializer import ServiceSerializer


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the SubscriptionPlan model.
    """

    services = ServiceSerializer(many=True, read_only=True)
    plan_services = serializers.PrimaryKeyRelatedField(
        queryset=PlanService.objects.all(), write_only=True, many=True
    )

    class Meta:
        """
        Meta class for SubscriptionPlanSerializer.
        """

        model = SubscriptionPlan
        fields = [
            "id",
            "plan_name",
            "plan_price",
            "number_tokens",
            "number_free_tokens",
            "active",
            "free_plan",
            "services",
            "plan_services",
        ]
