"""
Module containing AdminSerializer class.

This module provides a serializer for the Admin model, including nested serialization for the ArchimatchUser model.

Classes:
    AdminSerializer: Serializer for the Admin model with nested ArchimatchUser.
"""

from rest_framework import serializers

from app.users.models import Admin
from app.users.models import ArchimatchUser
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


class AdminSerializer(serializers.ModelSerializer):
    """
    Serializer for the Admin model.

    This serializer includes nested serialization for the ArchimatchUser model and manages admin-specific fields.

    Fields:
        id: The unique identifier of the admin.
        super_user: Boolean indicating if the admin is a superuser.
        user: Nested serializer for the ArchimatchUser associated with the admin.
        rights: List of rights/permissions for the admin. (write-only)
    """

    user = ArchimatchUserSerializer()
    rights = serializers.ListField(
        child=serializers.CharField(max_length=100), required=True, write_only=True
    )

    class Meta:
        """
        Meta class for AdminSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Admin
        fields = ["id", "super_user", "user", "rights"]

    def create(self, validated_data):
        """
        Create a new Admin instance.

        This method handles the creation of a new Admin instance, including the nested ArchimatchUser and setting permissions.

        Args:
            validated_data (dict): The validated data for creating the admin instance.

        Returns:
            Admin: The newly created Admin instance.
        """
        rights = validated_data.pop("rights", [])
        user_data = validated_data.pop("user")
        user = ArchimatchUser.objects.create(**user_data)
        admin = Admin.objects.create(user=user, **validated_data)
        admin.set_permissions(rights)
        return admin

    def update(self, instance, validated_data):
        """
        Update an existing Admin instance.

        This method handles the update of an Admin instance, including the nested ArchimatchUser and updating permissions.

        Args:
            instance (Admin): The existing admin instance to update.
            validated_data (dict): The validated data for updating the admin instance.

        Returns:
            Admin: The updated Admin instance.
        """
        rights = validated_data.pop("rights", None)
        user_data = validated_data.pop("user", None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()
        if rights is not None:
            instance.permissions.clear()
            instance.set_permissions(rights)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        Customize the representation of an Admin instance.

        This method customizes the serialized representation of an Admin instance, including handling superuser rights.

        Args:
            instance (Admin): The admin instance to represent.

        Returns:
            dict: The customized serialized representation of the admin instance.
        """
        data = super().to_representation(instance)
        if instance.super_user:
            data["rights"] = ["__All__"]
        else:
            data["rights"] = list(instance.permissions.values_list("codename", flat=True))
        return data
