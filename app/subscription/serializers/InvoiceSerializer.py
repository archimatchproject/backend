"""
Module containing the serializer for the Invoice model.

This module defines the InvoiceSerializer, which is responsible for serializing and
deserializing Invoice instances for use in API views.

Classes:
    InvoiceSerializer: Serializer class for the Invoice model.
"""

from rest_framework import serializers

from app.subscription.models.Invoice import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Invoice model.

    This class handles serialization and deserialization of Invoice instances,
    converting them to and from JSON for API responses and requests.
    """

    class Meta:
        """
        Meta class for the InvoiceSerializer.

        Attributes:
            model (type): The model that this serializer class is based on.
            fields (str): Specifies that all fields of the Invoice model should be included.
        """

        model = Invoice
        fields = "__all__"
