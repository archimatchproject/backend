"""
Module containing the UnavailabilitySerializer.

This module defines the UnavailabilitySerializer, which handles the serialization
and deserialization of Unavailability instances, including validation and custom
creation and update logic. The serializer is designed to work with time slots 
represented as strings and supports whole-day unavailability.
"""

from rest_framework import serializers
from app.architect_request import TIME_SLOT_CHOICES
from app.users.models.Unavailability import Unavailability
from app.users.models.Admin import Admin
from app.users.models.TimeSlot import TimeSlot
from datetime import datetime

class UnavailabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for the Unavailability model.

    The UnavailabilitySerializer handles the serialization and deserialization of
    Unavailability instances. It allows time slots to be specified as a list of strings,
    validates these strings against a predefined set of valid time slots, and includes
    custom logic for handling whole-day unavailability.

    Attributes:
        time_slots (ListField): A list of time slot strings for partial-day unavailability.
        whole_day (BooleanField): Indicates whether the entire day is marked as unavailable.

    Methods:
        validate_time_slots(value): Validates that each provided time slot string is valid.
        create(validated_data): Creates an Unavailability instance based on validated data.
        update(instance, validated_data): Updates an existing Unavailability instance.
        to_representation(instance): Customizes the representation of the Unavailability instance.
    """

    admin = serializers.PrimaryKeyRelatedField(
        queryset=Admin.objects.all()
    )
    time_slots = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True,
    )
    whole_day = serializers.BooleanField(required=False)

    class Meta:
        model = Unavailability
        fields = ['id', 'admin', 'date', 'time_slots', 'whole_day']

    def validate(self, data):
        """
        Override the validate method to ensure that `time_slots` is validated based on `whole_day`.
        """
        data = super().validate(data)
        whole_day = data.get('whole_day', False)
        time_slots = data.get('time_slots', None)

        if not whole_day and time_slots is None:
            raise serializers.ValidationError(
                "If `whole_day` is not true, `time_slots` must be provided."
            )

        if time_slots is not None:
            data['time_slots'] = self.validate_time_slots(time_slots)

        return data

    def validate_time_slots(self, value):
        """
        Validate that each time slot string corresponds to a valid time slot and conforms to the valid time format.
        """
        if value is None:
            return value

        valid_time_format = "%H:%M"
        
        valid_time_slots = [slot.time.strftime(valid_time_format) for slot in TimeSlot.objects.all()]

        invalid_slots = []
        for slot in value:
            try:
                time_obj = datetime.strptime(slot, valid_time_format)
                formatted_slot = time_obj.strftime(valid_time_format)
            except ValueError:
                invalid_slots.append(slot)
                continue

            if formatted_slot not in valid_time_slots:
                invalid_slots.append(slot)

        if invalid_slots:
            raise serializers.ValidationError(
                f"Invalid time slots or format: {', '.join(invalid_slots)}"
            )
        return value

    def create(self, validated_data):
        """
        Create a new Unavailability instance and handle many-to-many relationships.
        """
        time_slots = validated_data.pop('time_slots', [])
        whole_day = validated_data.get('whole_day', False)

        unavailability = Unavailability.objects.create(**validated_data)

        if whole_day:
            unavailability.time_slots.set(TimeSlot.objects.all())
        else:
            time_slot_objs = [TimeSlot.objects.get(time=slot) for slot in time_slots]
            unavailability.time_slots.set(time_slot_objs)

        return unavailability

    def update(self, instance, validated_data):
        """
        Update an existing Unavailability instance and handle many-to-many relationships.
        """
        time_slots = validated_data.pop('time_slots', [])
        whole_day = validated_data.get('whole_day', False)

        instance.date = validated_data.get('date', instance.date)
        instance.whole_day = validated_data.get('whole_day', instance.whole_day)

        if whole_day:
            instance.time_slots.set(TimeSlot.objects.all())
        else:
            time_slot_objs = [TimeSlot.objects.get(time=slot) for slot in time_slots]
            instance.time_slots.set(time_slot_objs)

        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Customizes the representation of the Unavailability instance.
        """
        representation = super().to_representation(instance)
        representation['time_slots'] = [slot.time.strftime('%H:%M') for slot in instance.time_slots.all()]
        return representation