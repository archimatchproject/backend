"""
Module containing ArchitectSerializer class.

This module provides a serializer for the Architect model, including nested serialization for the
 ArchimatchUser model.

Classes:
    ArchitectSerializer: Serializer for the Architect model with nested ArchimatchUser.
"""

from rest_framework import serializers

from app.users.models import Architect
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


class ArchitectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Architect model.

    This serializer includes nested serialization for the ArchimatchUser model and manages
    architect-specific fields.

    Fields:
        user: Nested serializer for the ArchimatchUser associated with the architect.
    """

    user = ArchimatchUserSerializer(required=True)

    class Meta:
        """
        Meta class for ArchitectSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Architect
        fields = "__all__"
