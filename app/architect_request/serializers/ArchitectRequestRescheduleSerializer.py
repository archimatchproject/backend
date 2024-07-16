"""
Module containing serializers for the ArchitectRequest model.

This module defines the serializers used for validating and serializing data
for the ArchitectRequest model, including CRUD operations and custom actions.

Classes:
    ArchitectRequestRescheduleSerializer: Serializer for rescheduling an ArchitectRequest.
"""

from rest_framework import serializers


class ArchitectRequestRescheduleSerializer(serializers.Serializer):
    """
    Serializer for rescheduling an ArchitectRequest.

    This serializer handles the validation and serialization of data required to
    reschedule an ArchitectRequest, including the date and time_slot fields.

    Attributes:
        date (DateField): The new date for the ArchitectRequest.
        time_slot (TimeField): The new time slot for the ArchitectRequest.
    """

    date = serializers.DateField(required=True)
    time_slot = serializers.TimeField(required=True)
