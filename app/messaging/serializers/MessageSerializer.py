"""
This module defines the serializers for the messaging system, converting Message model instances
 to and from JSON format for API usage.
"""

from django.db import models

from rest_framework import serializers

from app.messaging.models.Message import Message
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.Client import Client
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


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

    recipient_id = serializers.PrimaryKeyRelatedField(queryset=ArchimatchUser.objects.all(), write_only=True)
    sender = serializers.EmailField(source="sender.email", read_only=True)
    recipient = serializers.EmailField(source="recipient.email", read_only=True)
    recipient_user = ArchimatchUserSerializer(read_only=True)

    class Meta:
        """
        Meta class for the MessageSerializer.

        Meta Attributes:
            model (Message): The model that is being serialized.
            fields (list): The fields to be included in the serialized output.
        """

        model = Message
        fields = [
            "sender",
            "recipient",
            "recipient_id",
            "content",
            "timestamp",
            "recipient_user",
        ]


class ClientMessageSerializer(serializers.ModelSerializer):
    """
    ClientMessageSerializer is a ModelSerializer for the Client model. It includes the following fields:
        - id: The unique identifier for the client.
        - user: The user associated with the client.
        - last_message: The most recent message exchanged between the user and the client, read-only.
    Methods:
        - get_last_message(client): Retrieves the last message exchanged between the user and the given client.
    Meta:
        - model: The Client model that this serializer is based on.
        - fields: A list of fields to be included in the serialized output.
    """

    last_message = MessageSerializer(read_only=True)

    class Meta:
        """
        Meta class for the MessageSerializer.
        Attributes:
            model (Client): The model that this serializer is based on.
            fields (list): A list of fields to be included in the serialized output.
                           Adjust the fields based on your Client model.
        """

        model = Client
        fields = [
            "id",
            "user",
            "last_message",
        ]

    def get_last_message(self, client):
        """
        Retrieves the last message exchanged between the user and the given client.
        """
        user = self.context.get("user")

        last_message = (
            Message.objects.filter(
                (models.Q(sender=user) & models.Q(recipient=client.user))
                | (models.Q(sender=client.user) & models.Q(recipient=user))
            )
            .order_by("-timestamp")
            .first()
        )

        return last_message


class UserMessagesClientsSerializer(serializers.Serializer):
    """
    Serializer that returns a list of clients who have messages exchanged with the provided user.
    """

    user = serializers.PrimaryKeyRelatedField(queryset=ArchimatchUser.objects.all())
    clients = ClientMessageSerializer(many=True)

    def get_clients(self, user):
        """
        Retrieves clients that have exchanged messages with the provided user.
        """
        sent_messages = Message.objects.filter(sender=user)
        received_messages = Message.objects.filter(recipient=user)

        client_ids = set()
        for message in sent_messages:
            client_ids.add(message.recipient.id)
        for message in received_messages:
            client_ids.add(message.sender.id)

        clients = Client.objects.filter(user__in=client_ids)

        return clients

    def to_representation(self, instance):
        """
        Customize how the data is returned.
        """
        clients = self.get_clients(instance.user)

        return {
            "user": instance.user.id,
            "clients": ClientMessageSerializer(clients, many=True, context=self.context).data,
        }
