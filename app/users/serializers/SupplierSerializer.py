"""
Module containing SupplierSerializer class.

This module provides a serializer for the Supplier model, including nested serialization for
 the ArchimatchUser and SupplierSocialMedia models.

Classes:
    SupplierSerializer: Serializer for the Supplier model with nested ArchimatchUser and
     SupplierSocialMedia.
"""

from rest_framework import serializers

from app.users.models import Supplier
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer
from app.users.serializers.SupplierSocialMediaSerializer import SupplierSocialMediaSerializer
from app.users.serializers.SupplierSpecialitySerializer import SupplierSpecialitySerializer


class SupplierSerializer(serializers.ModelSerializer):
    """
    Serializer for the Supplier model.

    This serializer includes nested serialization for the ArchimatchUser and
    SupplierSocialMedia models.

    Fields:
        user: Nested serializer for the ArchimatchUser associated with the
        supplier.
        social_links: Nested serializer for the SupplierSocialMedia associated
        with the supplier.
        speciality_type: Nested serializer for the SupplierSpeciality associated
        with the supplier.
    """

    user = ArchimatchUserSerializer(required=True)
    social_links = SupplierSocialMediaSerializer()
    speciality_type = SupplierSpecialitySerializer(many=True)

    class Meta:
        """
        Meta class for SupplierSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Supplier
        fields = "__all__"
