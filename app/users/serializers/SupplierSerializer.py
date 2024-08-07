"""
Module containing SupplierSerializer class.

This module provides a serializer for the Supplier model, including nested serialization for
 the ArchimatchUser and SupplierSocialMedia models.

Classes:
    SupplierSerializer: Serializer for the Supplier model with nested ArchimatchUser and
     SupplierSocialMedia.
"""

from rest_framework import serializers

from app.catalogue.serializers.CollectionSerializer import CollectionSerializer
from app.core.models.SupplierSpeciality import SupplierSpeciality
from app.core.serializers.SupplierSpecialitySerializer import SupplierSpecialitySerializer
from app.users.models.Supplier import Supplier
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer
from app.users.serializers.SupplierSocialMediaSerializer import SupplierSocialMediaSerializer


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
    supplier_collections = CollectionSerializer(many=True)

    class Meta:
        """
        Meta class for SupplierSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Supplier
        fields = "__all__"


class SupplierInputSerializer(serializers.ModelSerializer):
    """
    Serializer for the Supplier model.

    This serializer includes nested serialization for the ArchimatchUser and
    SupplierSocialMedia models.

    Fields:
        user_phone_number: Phone number from the ArchimatchUser associated with the supplier.
        social_links: Nested serializer for the SupplierSocialMedia associated
        with the supplier.
        speciality_type: Array of IDs for the SupplierSpeciality associated
        with the supplier.
    """

    phone_number = serializers.CharField(source="user.phone_number")
    email = serializers.CharField(source="user.email")
    speciality_type = serializers.PrimaryKeyRelatedField(
        queryset=SupplierSpeciality.objects.all(),
        many=True,
    )

    class Meta:
        """
        Meta class for SupplierSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Supplier
        fields = (
            "id",
            "company_address",
            "company_speciality",
            "speciality_type",
            "phone_number",
            "email",
            "appearance",
        )


class SupplierPersonalInformationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Supplier model.

    This serializer includes nested serialization for the ArchimatchUser and
    SupplierSocialMedia models.

    Fields:
        user_phone_number: Phone number from the ArchimatchUser associated with the supplier.
        social_links: Nested serializer for the SupplierSocialMedia associated
        with the supplier.
        speciality_type: Array of IDs for the SupplierSpeciality associated
        with the supplier.
    """

    phone_number = serializers.CharField(source="user.phone_number")

    class Meta:
        """
        Meta class for SupplierSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Supplier
        fields = ("id", "company_address", "company_speciality", "phone_number", "company_name")
