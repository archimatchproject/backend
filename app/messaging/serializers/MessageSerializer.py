"""
This module defines the serializers for the messaging system, converting Message model instances
 to and from JSON format for API usage.
"""

from fcm_django.models import FCMDevice
from rest_framework import serializers

from app.messaging.models.Message import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model, handling conversion between Message instances
    and JSON data for API interactions.

    Fields:
    - sender_device (EmailField): Read-only reference to the email of the user associated
    with the sending device.
    - recipient_device (PrimaryKeyRelatedField): Write-only reference to the FCM device
    that receives the message.
    - sender (EmailField): Read-only reference to the email of the user associated with
    the sending device.
    - recipient (EmailField): Read-only reference to the email of the user associated
    with the receiving device.
    - content (CharField): The content of the message.
    - timestamp (DateTimeField): The timestamp when the message was sent, automatically
    generated.
    """

    recipient_device = serializers.PrimaryKeyRelatedField(
        queryset=FCMDevice.objects.all(), write_only=True
    )
    sender = serializers.EmailField(source="sender_device.user.email", read_only=True)
    recipient = serializers.EmailField(source="recipient_device.user.email", read_only=True)

    class Meta:
        """
        Meta class for the MessageSerializer.

        Meta Attributes:
            model (Message): The model that is being serialized.
            fields (list): The fields to be included in the serialized output.
        """

        model = Message
        fields = ["sender", "recipient", "recipient_device", "content", "timestamp"]
