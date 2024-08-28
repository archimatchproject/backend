"""
Module containing the UnavailabilitySerializer.

This module defines the UnavailabilitySerializer, which handles the serialization
and deserialization of Unavailability instances, including validation and custom
creation and update logic. The serializer is designed to work with time slots 
represented as strings and supports whole-day unavailability.
"""

from rest_framework import serializers
from app.architect_request import TIME_SLOT_CHOICES
from app.users.models.Meeting import Meeting
from app.users.models.Admin import Admin
from app.users.models.TimeSlot import TimeSlot
from datetime import datetime
from rest_framework.exceptions import ValidationError

class MeetingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Meeting model.

    The MeetingSerializer handles the serialization and deserialization of
    Meeting instances. It allows time slots to be specified as a list of strings,
    validates these strings against a predefined set of valid time slots, and includes
    custom logic for handling whole-day Meeting.

    Attributes:
        time_slots (ListField): A list of time slot strings for partial-day Meeting.
        whole_day (BooleanField): Indicates whether the entire day is marked as unavailable.

    Methods:
        validate_time_slots(value): Validates that each provided time slot string is valid.
        create(validated_data): Creates an Meeting instance based on validated data.
        update(instance, validated_data): Updates an existing Meeting instance.
        to_representation(instance): Customizes the representation of the Meeting instance.
    """

    admin = serializers.PrimaryKeyRelatedField(
        queryset=Admin.objects.all()
    )
    time = serializers.CharField()

    class Meta:
        model = Meeting
        fields = ['first_name', 'last_name', 'phone_number', 'admin', 'date', 'time', 'status']

    def validate(self, data):
        """
        Override the validate.
        """
    
        data = super().validate(data)
        admin = data.get('admin')
        date = data.get('date')
        time_slot = data.get("time",None)
        if time_slot is None:
            raise ValidationError(f"time slot is required")
        
        time_slot = self.validate_time_slot(data.get('time'))
        
        # Check for duplicate meetings
        if Meeting.objects.filter(admin=admin, date=date, time=time_slot).exists():
            raise ValidationError(f"A meeting already exists for admin {admin} on {date} at {time_slot.time.strftime('%H:%M')}")
        
        if time_slot is not None:
            data['time'] = time_slot
            
        return data

        

        return data

    def validate_time_slot(self, value):
        """
        Validate that the given time slot string corresponds to a valid time slot.
        """
        if value is None:
            return value

        valid_time_format = "%H:%M"

        try:
            time_obj = datetime.strptime(value, valid_time_format)
            formatted_slot = time_obj.strftime(valid_time_format)
        except ValueError:
            raise serializers.ValidationError(f"Invalid time format: {value}")

        try:
            time_slot = TimeSlot.objects.get(time=formatted_slot)
        except TimeSlot.DoesNotExist:
            raise ValidationError(f"Invalid time slot: {value}")

        return time_slot

    
    def to_representation(self, instance):
        """
        Customizes the representation of the Meeting instance.
        """
        representation = super().to_representation(instance)
        representation['time'] = instance.time.time.strftime('%H:%M')
        return representation