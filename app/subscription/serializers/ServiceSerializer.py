"""
Serializer module for the Service model.
"""

from rest_framework import serializers

from app.subscription.models.PlanService import PlanService


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Service model.
    """

    class Meta:
        """
        Meta class for ServiceSerializer.
        """

        model = PlanService
        fields = ["id", "description", "permissions"]
