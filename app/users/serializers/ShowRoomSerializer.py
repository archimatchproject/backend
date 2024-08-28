"""
Module containing ShowRoom Serializers class.

This module provides a serializer for the ShowRoom model

Classes:
    ShowRoomSerializer: Serializer for the Supplier model
"""
from rest_framework import serializers
from app.users.models.ShowRoom import ShowRoom

class ShowRoomSerializer(serializers.ModelSerializer):
    """
    Serializer for the Showroom model.

    Fields:
        address: The address of the showroom.
        phone_number: The phone number of the showroom.
    """

    class Meta:
        """
        Meta class for ShowroomSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """
        model = ShowRoom
        fields = ("id", "address", "phone_number")