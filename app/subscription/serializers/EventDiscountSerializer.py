"""
Serializers for the subscription models.
"""

from rest_framework import serializers
from app.subscription.models import EventDiscount

class EventDiscountSerializer(serializers.ModelSerializer):
    """
    Serializer for the EventDiscount model.

    This serializer handles the serialization and deserialization of
    EventDiscount instances. It is used to represent discount events 
    such as Black Friday, Eid, etc., which apply a percentage discount 
    on subscription plans within a specified date range.
    """

    class Meta:
        """
        Meta class for EventDiscountSerializer.
        
        Defines the model to serialize and the fields to include in the 
        serialized output.
        """
        model = EventDiscount
        fields = [
            'id',
            'event_name',
            'discount_percentage',
            'start_date',
            'end_date',
        ]