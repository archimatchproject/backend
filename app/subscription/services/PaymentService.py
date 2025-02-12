"""
Service module for the Payment model.

This module defines the service for handling the business logic and exceptions
related to Payment creation and management.

Classes:
    PaymentService: Service class for Payment operations.
"""


from django.db import transaction


from app.subscription import PAYMENT_METHOD_CHOICES
from app.subscription.models import ArchitectPayment
from app.subscription.models.ArchitectInvoice import ArchitectInvoice
from app.subscription.models.ArchitectSelectedSubscriptionPlan import (
    ArchitectSelectedSubscriptionPlan,
)
from app.subscription.models.SupplierInvoice import SupplierInvoice
from app.subscription.models.SupplierPayment import SupplierPayment
from app.subscription.models.SupplierSelectedSubscriptionPlan import (
    SupplierSelectedSubscriptionPlan,
)
from app.subscription.serializers.InvoiceSerializer import (
    ArchitectInvoiceSerializer,
    SupplierInvoiceSerializer,
)
from app.subscription.serializers.PaymentSerializer import (
    ArchitectPaymentPOSTSerializer,
    ArchitectPaymentSerializer,
    OfficePaymentPOSTSerializer,
    SupplierPaymentPOSTSerializer,
    SupplierPaymentSerializer,
)
from app.users.models.Architect import Architect
from app.users.models.Supplier import Supplier
from datetime import datetime, timedelta
from app.users.models.Office import Office
from app.subscription.models.OfficeSelectedSubscriptionPlan import OfficeSelectedSubscriptionPlan
from app.subscription.models.OfficePayment import OfficePayment
from app.subscription.models.OfficeInvoice import OfficeInvoice


class PaymentService:
    """
    Service class for handling Payment operations.

    Handles business logic and exception handling for Payment creation and management.

    Methods:
        create_payment(request, data): Handles validation and creation of a new Payment.
    """

    @classmethod
    def create_architect_payment(cls, request, data):
        """
        Handles validation and creation of a new Payment, and subsequently creates an Invoice.

        Args:
            request (Request): The request object containing the authenticated user.
            data (dict): The validated data for creating a Payment instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        annual = data.pop("annual_payment", False)
        serializer = ArchitectPaymentPOSTSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Set start_date to today and end_date to 30 days from today
        start_date = datetime.today().date()
        end_date = start_date + timedelta(days=30)

        user = request.user

        architect = Architect.objects.get(user=user)
        subscription_plan = validated_data.get("subscription_plan")

        # Create the SelectedSubscriptionPlan
        selected_plan_data = {
            "plan_name": subscription_plan.plan_name,
            "plan_price": (
                subscription_plan.get_annual_price()
                if annual
                else subscription_plan.get_effective_price()
            ),
            "number_tokens": subscription_plan.number_tokens + subscription_plan.number_free_tokens,
            "remaining_tokens": subscription_plan.number_tokens
            + subscription_plan.number_free_tokens,
            "active": subscription_plan.active,
            "free_plan": subscription_plan.free_plan,
            "start_date": start_date,
            "end_date": end_date,
            "discount": subscription_plan.discount,
            "discount_percentage": subscription_plan.discount_percentage,
        }
        selected_plan = ArchitectSelectedSubscriptionPlan.objects.create(**selected_plan_data)

        # Add services to the SelectedSubscriptionPlan
        selected_plan.services.set(subscription_plan.services.all())

        architect.subscription_plan = selected_plan
        architect.save()

        with transaction.atomic():
            payment = ArchitectPayment.objects.create(
                architect=architect,
                subscription_plan=selected_plan,
                payment_method=validated_data.get("payment_method"),
                status="Paid",
            )

            invoice = ArchitectInvoice(
                invoice_number=f"INV-{payment.id}",
                architect=architect,
                plan_name=selected_plan.plan_name,
                plan_price=selected_plan.plan_price,
                discount=selected_plan.discount,
                discount_percentage=(
                    selected_plan.discount_percentage if selected_plan.discount else None
                ),
                discount_message=(
                    selected_plan.discount_message if selected_plan.discount else ""
                ),
            )
            invoice.save()

            return (
                True,
                {
                    "payment": ArchitectPaymentSerializer(payment).data,
                    "invoice": ArchitectInvoiceSerializer(invoice).data,
                },
            )

    @classmethod
    def get_payment_methods(cls):
        """
        Returns the payment methods as label-value objects.

        Returns:
            Response: The response object containing the payment methods.
        """
        payment_methods = [
            {"label": label, "value": value} for value, label in PAYMENT_METHOD_CHOICES
        ]
        return True, payment_methods

    @classmethod
    def create_supplier_payment(cls, request, data):
        """
        Handles validation and creation of a new Payment, and subsequently creates an Invoice.

        Args:
            request (Request): The request object containing the authenticated user.
            data (dict): The validated data for creating a Payment instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        annual = data.pop("annual_payment", False)

        serializer = SupplierPaymentPOSTSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user

        supplier = Supplier.objects.get(user=user)
        subscription_plan = validated_data.pop("subscription_plan")

        # Create the SelectedSubscriptionPlan
        selected_plan_data = {
            "plan_name": subscription_plan.plan_name,
            "plan_price": (
                subscription_plan.get_annual_price()
                if annual
                else subscription_plan.get_effective_price()
            ),
            "collection_number": subscription_plan.collection_number,
            "product_number_per_collection": subscription_plan.product_number_per_collection,
            "active": subscription_plan.active,
            "free_plan": subscription_plan.free_plan,
            "start_date": subscription_plan.start_date,
            "end_date": subscription_plan.end_date,
            "discount": subscription_plan.discount,
            "discount_percentage": subscription_plan.discount_percentage,
        }
        selected_plan = SupplierSelectedSubscriptionPlan.objects.create(**selected_plan_data)

        supplier.subscription_plan = selected_plan
        supplier.save()

        with transaction.atomic():
            payment = SupplierPayment.objects.create(
                supplier=supplier,
                subscription_plan=selected_plan,
                payment_method=validated_data.get("payment_method"),
                status="Paid",
            )
            invoice = SupplierInvoice(
                invoice_number=f"INV-{payment.id}",
                supplier=supplier,
                plan_name=selected_plan.plan_name,
                plan_price=selected_plan.plan_price,
                discount=selected_plan.discount,
                discount_percentage=(
                    selected_plan.discount_percentage if selected_plan.discount else None
                ),
                discount_message=(
                    selected_plan.discount_message if selected_plan.discount else ""
                ),
            )
            invoice.save()

            return True, {
                "payment": SupplierPaymentSerializer(payment).data,
                "invoice": SupplierInvoiceSerializer(invoice).data,
            }

    @classmethod
    def create_office_payment(cls, request, data):
        """
        Handles validation and creation of a new OfficePayment, and subsequently
        creates an OfficeInvoice.

        Args:
            request (Request): The request object containing the authenticated user.
            data (dict): The validated data for creating a Payment instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        annual = data.pop("annual_payment", False)
        serializer = OfficePaymentPOSTSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Set start_date to today and end_date to 30 days from today (adjust as necessary)
        start_date = datetime.today().date()
        end_date = start_date + timedelta(days=30)

        user = request.user

        office = Office.objects.get(user=user)
        subscription_plan = validated_data.get("subscription_plan")

        # Create the SelectedSubscriptionPlan
        selected_plan_data = {
            "plan_name": subscription_plan.plan_name,
            "plan_price": (
                subscription_plan.get_annual_price()
                if annual
                else subscription_plan.get_effective_price()
            ),
            "active": subscription_plan.active,
            "announces_number": subscription_plan.announces_number,
            "architects_number_per_announce": subscription_plan.architects_number_per_announce,
            "free_plan": subscription_plan.free_plan,
            "start_date": start_date,
            "end_date": end_date,
            "discount": subscription_plan.discount,
            "discount_percentage": subscription_plan.discount_percentage,
        }
        selected_plan = OfficeSelectedSubscriptionPlan.objects.create(**selected_plan_data)

        office.subscription_plan = selected_plan
        office.save()

        with transaction.atomic():
            payment = OfficePayment.objects.create(
                office=office,
                subscription_plan=selected_plan,
                payment_method=validated_data.get("payment_method"),
                status="Paid",
            )
            invoice = OfficeInvoice(
                invoice_number=f"INV-{payment.id}",
                office=office,
                plan_name=selected_plan.plan_name,
                plan_price=selected_plan.plan_price,
                discount=selected_plan.discount,
                discount_percentage=(
                    selected_plan.discount_percentage if selected_plan.discount else None
                ),
                discount_message=(selected_plan.discount_message if selected_plan.discount else ""),
            )
            invoice.save()

            return (
                True,
                {},
            )
