"""
Module containing the Budget serializer.

This module defines the serializer for the Budget model, which converts
the model instances to and from JSON format for API communication.

Serializers:
    BudgetSerializer: Serializer for the Budget model.
"""

from rest_framework import serializers

from app.core.models.Budget import Budget


class BudgetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Budget model.

    Serializes Budget model instances to and from JSON format.
    """

    class Meta:
        """
        Meta class for BudgetSerializer.

        Defines the model and fields to be included in the serialization.

        Attributes:
            model (Budget): The model class associated with this serializer.
            fields (list): List of fields to be included in the serialized representation.
        """

        model = Budget
        fields = ["id", "name"]
