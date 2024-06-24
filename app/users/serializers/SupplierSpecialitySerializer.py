"""
Module containing SupplierSpeciality Serializer class.

This module provides a serializer for the SupplierSpeciality  model, including nested serialization for the ArchimatchUser model.

Classes:
    SupplierSpeciality Serializer: Serializer for the SupplierSpeciality  model with nested ArchimatchUser.
"""
from rest_framework import serializers

from app.users.models import SupplierSpeciality


class SupplierSpecialitySerializer(serializers.ModelSerializer):
    """
    Serializer for the SupplierSpeciality  model.

    This serializer includes nested serialization for the ArchimatchUser model and manages SupplierSpeciality -specific fields.

    Fields:
        user: Nested serializer for the ArchimatchUser associated with the SupplierSpeciality .
    """

    class Meta:
        """
        Meta class for SupplierSpeciality Serializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = SupplierSpeciality
        fields = ["id", "label", "icon"]
