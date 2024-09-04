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

    services = serializers.SerializerMethodField(read_only=True)
    plan_services = serializers.PrimaryKeyRelatedField(
        queryset=PlanService.objects.all(), write_only=True, many=True
    )
    effective_price = serializers.SerializerMethodField()
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
            "effective_price"
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
    
    def get_effective_price(self, obj):
        return obj.get_effective_price()
        
class SupplierSubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the SupplierSubscriptionPlan model.
    """
    effective_price = serializers.SerializerMethodField()
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
            "effective_price"
        ]
    
    def get_effective_price(self, obj):
        return obj.get_effective_price()