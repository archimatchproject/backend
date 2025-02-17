"""
Serializer module for the Payment model.
"""

from rest_framework import serializers

from app.core.serializers.NoteSerializer import NoteSerializer
from app.subscription.models.ArchitectPayment import ArchitectPayment
from app.subscription.models.ArchitectSelectedSubscriptionPlan import ArchitectSelectedSubscriptionPlan
from app.subscription.models.ArchitectSubscriptionPlan import ArchitectSubscriptionPlan
from app.subscription.models.OfficePayment import OfficePayment
from app.subscription.models.OfficeSelectedSubscriptionPlan import OfficeSelectedSubscriptionPlan
from app.subscription.models.OfficeSubscriptionPlan import OfficeSubscriptionPlan
from app.subscription.models.Payment import Payment
from app.subscription.models.SupplierSelectedSubscriptionPlan import SupplierSelectedSubscriptionPlan
from app.subscription.models.SupplierSubscriptionPlan import SupplierSubscriptionPlan
from app.subscription.serializers.SelectedSubscriptionPlanSerializer import ArchitectSelectedSubscriptionPlanSerializer
from app.subscription.serializers.SelectedSubscriptionPlanSerializer import OfficeSelectedSubscriptionPlanSerializer
from app.subscription.serializers.SelectedSubscriptionPlanSerializer import SupplierSelectedSubscriptionPlanSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    """

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
            "notes",
        ]


class ArchitectPaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    """

    architect = serializers.EmailField(read_only=True)
    admin_responsable = serializers.EmailField(read_only=True)
    payment_subscription_plan = ArchitectSelectedSubscriptionPlanSerializer(source="subscription_plan", read_only=True)
    subscription_plan = serializers.PrimaryKeyRelatedField(
        queryset=ArchitectSelectedSubscriptionPlan.objects.all(), write_only=True
    )
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for PaymentSerializer.
        """

        model = ArchitectPayment
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
    payment_subscription_plan = SupplierSelectedSubscriptionPlanSerializer(source="subscription_plan", read_only=True)
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


class OfficePaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Office Payment model.
    """

    office = serializers.EmailField(read_only=True)
    admin_responsable = serializers.EmailField(read_only=True)
    payment_subscription_plan = OfficeSelectedSubscriptionPlanSerializer(source="subscription_plan", read_only=True)
    subscription_plan = serializers.PrimaryKeyRelatedField(
        queryset=OfficeSelectedSubscriptionPlan.objects.all(), write_only=True
    )
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for PaymentSerializer.
        Attributes:
            model (type): The model associated with the serializer, in this case, OfficePayment.
            fields (list): A list of fields to be included in the serialized output.
                - id: The unique identifier for the payment.
                - office: The office associated with the payment.
                - admin_responsable: The administrator responsible for the payment.
                - payment_method: The method used for the payment.
                - status: The current status of the payment.
                - payment_subscription_plan: The subscription plan associated with the payment.
                - subscription_plan: The subscription plan details.
                - notes: Additional notes regarding the payment.
        """

        model = OfficePayment
        fields = [
            "id",
            "office",
            "admin_responsable",
            "payment_method",
            "status",
            "payment_subscription_plan",
            "subscription_plan",
            "notes",
        ]


class ArchitectPaymentPOSTSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    """

    subscription_plan = serializers.PrimaryKeyRelatedField(
        queryset=ArchitectSubscriptionPlan.objects.all(), write_only=True
    )

    class Meta:
        """
        Meta class for PaymentSerializer.
        """

        model = Payment
        fields = [
            "payment_method",
            "subscription_plan",
        ]


class SupplierPaymentPOSTSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    """

    subscription_plan = serializers.PrimaryKeyRelatedField(
        queryset=SupplierSubscriptionPlan.objects.all(), write_only=True
    )

    class Meta:
        """
        Meta class for PaymentSerializer.
        """

        model = Payment
        fields = [
            "payment_method",
            "subscription_plan",
        ]


class OfficePaymentPOSTSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Payment for Office.
    """

    subscription_plan = serializers.PrimaryKeyRelatedField(
        queryset=OfficeSubscriptionPlan.objects.all(), write_only=True
    )

    class Meta:
        """
        Meta class for PaymentSerializer.
        Attributes:
            model (type): The model associated with the serializer.
            fields (list): List of fields to be included in the serialized output.
        """

        model = Payment
        fields = [
            "payment_method",
            "subscription_plan",
        ]
