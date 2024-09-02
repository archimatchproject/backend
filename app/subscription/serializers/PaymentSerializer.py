"""
Serializer module for the Payment model.
"""

from rest_framework import serializers

from app.core.serializers.NoteSerializer import NoteSerializer
from app.subscription.models.ArchitectSelectedSubscriptionPlan import ArchitectSelectedSubscriptionPlan
from app.subscription.models.Payment import Payment
from app.subscription.models.SelectedSubscriptionPlan import SelectedSubscriptionPlan
from app.subscription.models.SupplierSelectedSubscriptionPlan import SupplierSelectedSubscriptionPlan
from app.subscription.serializers.SubscriptionPlanSerializer import SubscriptionPlanSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    """
    admin_responsable = serializers.EmailField(read_only=True)
    payment_subscription_plan = SubscriptionPlanSerializer(
        source="subscription_plan", read_only=True
    )
    subscription_plan = serializers.PrimaryKeyRelatedField(
        queryset=SelectedSubscriptionPlan.objects.all(), write_only=True
    )
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for PaymentSerializer.
        """

        model = Payment
        fields = [
            "id",
            "admin_responsable",
            "payment_method",
            "status",
            "payment_subscription_plan",
            "subscription_plan",
            "notes",
        ]

class ArchitectPaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    """

    architect = serializers.EmailField(read_only=True)
    admin_responsable = serializers.EmailField(read_only=True)
    payment_subscription_plan = SubscriptionPlanSerializer(
        source="subscription_plan", read_only=True
    )
    subscription_plan = serializers.PrimaryKeyRelatedField(
        queryset=ArchitectSelectedSubscriptionPlan.objects.all(), write_only=True
    )
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for PaymentSerializer.
        """

        model = Payment
        fields = [
            "id",
            "architect",
            "admin_responsable",
            "payment_method",
            "status",
            "payment_subscription_plan",
            "subscription_plan",
            "notes",
        ]

class SupplierPaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    """

    supplier = serializers.EmailField(read_only=True)
    admin_responsable = serializers.EmailField(read_only=True)
    payment_subscription_plan = SubscriptionPlanSerializer(
        source="subscription_plan", read_only=True
    )
    subscription_plan = serializers.PrimaryKeyRelatedField(
        queryset=SupplierSelectedSubscriptionPlan.objects.all(), write_only=True
    )
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for PaymentSerializer.
        """

        model = Payment
        fields = [
            "id",
            "supplier",
            "admin_responsable",
            "payment_method",
            "status",
            "payment_subscription_plan",
            "subscription_plan",
            "notes",
        ]