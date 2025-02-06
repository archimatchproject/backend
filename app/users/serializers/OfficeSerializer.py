"""
Module containing OfficeSerializer class.

This module provides a serializer for the Office model, including nested serialization for
 the ArchimatchUser and OfficeSocialMedia models.

Classes:
    OfficeSerializer: Serializer for the Office model with nested ArchimatchUser and
     OfficeSocialMedia.
"""

from rest_framework import serializers

from app.users.models.Office import Office
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer
from app.users.serializers.ShowRoomSerializer import ShowRoomSerializer
from app.users.serializers.SupplierSocialMediaSerializer import SupplierSocialMediaSerializer


class OfficeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Office model.

    This serializer includes nested serialization for the ArchimatchUser and
    SupplierSocialMedia models.

    Fields:
        user: Nested serializer for the ArchimatchUser associated with the
        office.
        social_links: Nested serializer for the SupplierSocialMedia associated
        with the office.
    """

    user = ArchimatchUserSerializer(required=True)
    social_links = SupplierSocialMediaSerializer()

    class Meta:
        """
        Meta class for OfficeSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Office
        fields = "__all__"


class OfficeInputSerializer(serializers.ModelSerializer):
    """
    Serializer for the Office model.

    This serializer includes nested serialization for the ArchimatchUser and
    SupplierSocialMedia models.

    Fields:
        user_phone_number: Phone number from the ArchimatchUser associated with the office.
        social_links: Nested serializer for the SupplierSocialMedia associated
        with the office.
    """

    phone_number = serializers.CharField(source="user.phone_number")
    email = serializers.CharField(source="user.email")

    class Meta:
        """
        Meta class for OfficeSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Office
        fields = (
            "id",
            "office_address",
            "phone_number",
            "email",
        )


class OfficePersonalInformationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Office model.

    This serializer includes nested serialization for the ArchimatchUser and
    SupplierSocialMedia models.

    Fields:
        user_phone_number: Phone number from the ArchimatchUser associated with the office.
        social_links: Nested serializer for the SupplierSocialMedia associated
        with the office.
    """

    phone_number = serializers.CharField(source="user.phone_number")
    showrooms = ShowRoomSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for OfficeSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Office
        fields = ("id", "office_address", "phone_number", "office_name")
