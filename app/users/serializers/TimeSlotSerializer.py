from rest_framework import serializers
from app.users.models.TimeSlot import TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    """
    Serializer for the TimeSlot model.
    """
    class Meta:
        model = TimeSlot
        fields = ['time']