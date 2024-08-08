"""
Serializer for the Device model.

This serializer includes the ArchimatchUserSerializer to provide detailed user information
for each device.

Fields:
- id (IntegerField): The ID of the device.
- name (CharField): The name of the device.
- user (ArchimatchUserSerializer): The user associated with the device.
"""

from fcm_django.models import FCMDevice
from rest_framework import serializers

from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Device model.
    """

    user = ArchimatchUserSerializer(read_only=True)

    class Meta:
        """
        Meta class for the MessageSerializer.
        """

        model = FCMDevice
        fields = ["id", "name", "user"]
