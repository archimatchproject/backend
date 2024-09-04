"""
Serializer module for the SelectedSubscriptionPlan model.
"""

from rest_framework import serializers

from app.subscription.models.ArchitectSelectedSubscriptionPlan import ArchitectSelectedSubscriptionPlan
from app.subscription.models.PlanService import PlanService
from app.subscription.models.SelectedSubscriptionPlan import SelectedSubscriptionPlan
from app.subscription.models.SupplierSelectedSubscriptionPlan import SupplierSelectedSubscriptionPlan
from app.subscription.serializers.ServiceSerializer import ServiceSerializer


class SelectedSubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the SubscriptionPlan model.
    """

    
    plan_services = serializers.PrimaryKeyRelatedField(
        queryset=PlanService.objects.all(), write_only=True, many=True
    )

    class Meta:
        """
        Meta class for SelectedSubscriptionPlanSerializer.
        """

        model = SelectedSubscriptionPlan
        fields = [
            "id",
            "plan_name",
            "plan_price",
            "remaining_tokens",
            "active",
            "free_plan",
            "services",
            "plan_services",
            "start_date",
            "end_date",
        ]
    



class ArchitectSelectedSubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the SubscriptionPlan model.
    """

    services = serializers.SerializerMethodField()
    plan_services = serializers.PrimaryKeyRelatedField(
        queryset=PlanService.objects.all(), write_only=True, many=True
    )

    class Meta:
        """
        Meta class for SelectedSubscriptionPlanSerializer.
        """

        model = ArchitectSelectedSubscriptionPlan
        fields = [
            "id",
            "plan_name",
            "plan_price",
            "remaining_tokens",
            "active",
            "free_plan",
            "services",
            "plan_services",
            "start_date",
            "end_date",
        ]
    
    def get_services(self, obj):
        all_services = PlanService.objects.all()
        selected_services = obj.services.all()
        return [
            {
                "service": ServiceSerializer(service).data,
                "included": service in selected_services,
            }
            for service in all_services
        ]


class SupplierSelectedSubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the SubscriptionPlan model.
    """

    class Meta:
        """
        Meta class for SelectedSubscriptionPlanSerializer.
        """

        model = SupplierSelectedSubscriptionPlan
        fields = [
            "id",
            "plan_name",
            "plan_price",
            "collection_number",
            "product_number_per_collection",
            "active",
            "free_plan",
            "services",
            "plan_services",
            "start_date",
            "end_date",
        ]