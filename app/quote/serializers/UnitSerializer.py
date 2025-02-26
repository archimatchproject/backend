"""
UnitSerializer
This module defines the UnitSerializer class, which is a serializer for the Unit model.
It is used to represent the Unit model in API responses and to validate input data
for creating or updating a Unit instance.
Classes:
    UnitSerializer: A serializer for the Unit model.

"""

from rest_framework import serializers

from app.quote.models.Unit import Unit


class UnitSerializer(serializers.ModelSerializer):
    """
    Serializer for the Unit model.

    This serializer is used to represent the Unit model in the response and to
    validate input data for creating or updating a Unit instance.
    """

    class Meta:
        """
        Meta class for UnitSerializer.
        Attributes:
            model (Model): The model that is being serialized.
            fields (list): The list of fields to be included in the serialization.
        """

        model = Unit
        fields = ["id", "title"]
