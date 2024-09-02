"""
Serializer module for the SubscriptionPlan model.
"""

from rest_framework import serializers

from app.subscription.models.ArchitectSubscriptionPlan import ArchitectSubscriptionPlan
from app.subscription.models.PlanService import PlanService
from app.subscription.models.SubscriptionPlan import SubscriptionPlan
from app.subscription.models.SupplierSubscriptionPlan import SupplierSubscriptionPlan
from app.subscription.serializers.ServiceSerializer import ServiceSerializer


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the SubscriptionPlan model.
    """

    class Meta:
        """
        Meta class for SubscriptionPlanSerializer.
        """

        model = SubscriptionPlan
        fields = [
            "id",
            "plan_name",
            "plan_price",
            "active",
            "free_plan",
            "discount",
            "discount_percentage",
            "start_date",
            "end_date",
            "discount_message",
        ]


class ArchitectSubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the ArchitectSubscriptionPlan model.
    """

    services = ServiceSerializer(many=True, read_only=True)
    plan_services = serializers.PrimaryKeyRelatedField(
        queryset=PlanService.objects.all(), write_only=True, many=True
    )

    class Meta:
        """
        Meta class for ArchitectSubscriptionPlanSerializer.
        """

        model = ArchitectSubscriptionPlan
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
            "discount",
            "discount_percentage",
            "start_date",
            "end_date",
            "discount_message",
        ]
        
class SupplierSubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the SupplierSubscriptionPlan model.
    """

    class Meta:
        """
        Meta class for SupplierSubscriptionPlanSerializer.
        """

        model = SupplierSubscriptionPlan
        fields = [
            "id",
            "plan_name",
            "plan_price",
            "active",
            "free_plan",
            "collection_number",
            "product_number_per_collection",
            "discount",
            "discount_percentage",
            "start_date",
            "end_date",
            "discount_message",
        ]