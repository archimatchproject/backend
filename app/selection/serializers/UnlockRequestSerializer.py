"""
This module contains serializers for the UnlockRequest model.

The serializers included are:
- UnlockRequestSerializer: A serializer for converting UnlockRequest
instances to and from JSON format
, including nested Selection instances.
- UnlockRequestPostSerializer: A serializer for creating or updating UnlockRequest instances,
using primary keys for related Selection instances.

These serializers are used to handle the data representation and validation for UnlockRequest
objects in the application.
"""

from rest_framework import serializers

from app.selection.models.Selection import Selection
from app.selection.models.UnlockRequest import UnlockRequest
from app.selection.serializers.SelectionSerializer import SelectionSerializer


class UnlockRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the UnlockRequest model.
    This serializer handles the conversion of UnlockRequest instances to and from JSON format.
    It includes the following fields:
    - id: The unique identifier of the unlock request.
    - selection: A nested serializer for the related Selection instance.
    - message: A message associated with the unlock request.
    - status: The current status of the unlock request.
    """

    selection = SelectionSerializer()

    class Meta:
        """
        Meta class for the UnlockRequestSerializer.
        Attributes:
            model (type): The model associated with the serializer.
            fields (list): List of fields to be included in the serialized output.
        """

        model = UnlockRequest
        fields = ["id", "selection", "message", "status", "created_at"]


class UnlockRequestPostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating UnlockRequest instances.
    This serializer handles the conversion of UnlockRequest instances to and from JSON format.
    It includes the following fields:
    - id: The unique identifier of the unlock request.
    - selection: The primary key of the related Selection instance.
    - message: A message associated with the unlock request.
    - status: The current status of the unlock request.
    """

    selection = serializers.PrimaryKeyRelatedField(queryset=Selection.objects.all())

    class Meta:
        """
        Meta class for UnlockRequestSerializer.
        Attributes:
            model (type): The model associated with the serializer, in this case, UnlockRequest.
            fields (list): A list of fields to be included in the serialization process.
        """

        model = UnlockRequest
        fields = ["id", "selection", "message", "status"]
