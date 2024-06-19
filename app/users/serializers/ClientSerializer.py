"""
Module containing ClientSerializer class.

This module provides a serializer for the Client model, including nested serialization for the ArchimatchUser model.

Classes:
    ClientSerializer: Serializer for the Client model with nested ArchimatchUser.
"""

from rest_framework import serializers

from app.users.models import ArchimatchUser, Client
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client model.

    This serializer includes nested serialization for the ArchimatchUser model and manages client-specific fields.

    Fields:
        user: Nested serializer for the ArchimatchUser associated with the client.
    """

    user = ArchimatchUserSerializer()

    class Meta:
        """
        Meta class for ClientSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = Client
        fields = ["id", "user"]

    def create(self, validated_data):
        """
        Create a new Client instance.

        This method creates a new ArchimatchUser instance from the nested user data,
        then uses it to create and return a new Client instance.

        Args:
            validated_data (dict): The validated data from the serializer.

        Returns:
            Client: The created Client instance.
        """
        user_data = validated_data.pop("user")
        user = ArchimatchUser.objects.create(**user_data)
        client = Client.objects.create(user=user, **validated_data)
        return client

    def update(self, instance, validated_data):
        """
        Update an existing Client instance.

        This method updates the nested ArchimatchUser instance with the provided data,
        then updates and returns the Client instance.

        Args:
            instance (Client): The existing Client instance to update.
            validated_data (dict): The validated data from the serializer.

        Returns:
            Client: The updated Client instance.
        """
        user_data = validated_data.pop("user")
        user = instance.user

        instance.user.username = user_data.get("username", user.username)
        instance.user.first_name = user_data.get("first_name", user.first_name)
        instance.user.last_name = user_data.get("last_name", user.last_name)
        instance.user.email = user_data.get("email", user.email)
        instance.user.phone_number = user_data.get("phone_number", user.phone_number)
        instance.user.image = user_data.get("image", user.image)
        instance.user.user_type = user_data.get("user_type", user.user_type)
        instance.user.save()

        instance.save()
        return instance
