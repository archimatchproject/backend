"""
This module contains the TimeSlotSerializer class, which is used to serialize
and deserialize TimeSlot model instances.
Classes:
    TimeSlotSerializer: A serializer for the TimeSlot model.
Usage:
    This serializer can be used to convert TimeSlot model instances to and from
    JSON format, making it easier to work with TimeSlot data in APIs.
Example:
    time_slot_instance = TimeSlot.objects.get(id=1)
    serializer = TimeSlotSerializer(time_slot_instance)
    json_data = serializer.data
"""

from rest_framework import serializers

from app.users.models.TimeSlot import TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    """
    Serializer for the TimeSlot model.
    """

    class Meta:
        """
        Meta class for the TimeSlotSerializer.
        Attributes:
            model (django.db.models.Model): The model that is being serialized.
            fields (list): List of fields to be included in the serialization.
        """

        model = TimeSlot
        fields = ["time"]
