"""
Module containing serializers for the OfficeRequest model.

This module defines the serializers used for validating and serializing data
for the OfficeRequest model, including CRUD operations and custom actions.

Classes:
    OfficeRequestRescheduleSerializer: Serializer for rescheduling an OfficeRequest.
"""

from rest_framework import serializers


class OfficeRequestRescheduleSerializer(serializers.Serializer):
    """
    Serializer for rescheduling an OfficeRequest.

    This serializer handles the validation and serialization of data required to
    reschedule an OfficeRequest, including the date and time_slot fields.

    Attributes:
        date (DateField): The new date for the OfficeRequest.
        time_slot (TimeField): The new time slot for the OfficeRequest.
    """

    date = serializers.DateField(required=True)
    time_slot = serializers.TimeField(required=True)
