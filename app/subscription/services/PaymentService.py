"""
Service module for the Payment model.

This module defines the service for handling the business logic and exceptions
related to Payment creation and management.

Classes:
    PaymentService: Service class for Payment operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.subscription import PAYMENT_METHOD_CHOICES
from app.subscription.models.Payment import Payment
from app.subscription.serializers.PaymentSerializer import PaymentSerializer
from app.users.models.Architect import Architect


class PaymentService:
    """
    Service class for handling Payment operations.

    Handles business logic and exception handling for Payment creation and management.

    Methods:
        create_payment(request, data): Handles validation and creation of a new Payment.
    """

    @classmethod
    def create_payment(cls, request, data):
        """
        Handles validation and creation of a new Payment.

        Args:
            request (Request): The request object containing the authenticated user.
            data (dict): The validated data for creating a Payment instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = PaymentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        try:
            architect = Architect.objects.get(user=user)
            with transaction.atomic():
                # Create Payment instance
                payment = Payment.objects.create(architect=architect, **validated_data)

                return Response(
                    PaymentSerializer(payment).data,
                    status=status.HTTP_201_CREATED,
                )
        except Architect.DoesNotExist:
            raise NotFound(detail="Authenticated user is not an architect.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating payment: {str(e)}")

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
        return Response(payment_methods, status=status.HTTP_200_OK)
