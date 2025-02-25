"""
This module contains the ConversationSerializer class, which is responsible for serializing
the Conversation model. It includes related user, admins, and messages data. The serializer
uses custom methods to fetch and serialize messages exchanged between the user and admins.
Classes:
    ConversationSerializer: A serializer for the Conversation model, including related user,
                            admins, and messages data.
Methods:
    get_messages: Custom method to fetch all messages exchanged between the admins and the client.

"""

from django.db import models

from rest_framework import serializers

from app.messaging.models import Message
from app.messaging.models.Conversation import Conversation
from app.messaging.serializers.MessageSerializer import MessageSerializer
from app.users.serializers.AdminSerializer import AdminSerializer
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model, including admins, user, and messages.
    """

    user = ArchimatchUserSerializer()
    admins = AdminSerializer(many=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the ConversationSerializer.
        Attributes:
            model (type): The model that is being serialized, in this case, Conversation.
            fields (list): A list of fields to be included in the serialized output.
                           Includes "user", "admins", "messages", and "created_at".
        """

        model = Conversation
        fields = ["user", "admins", "messages", "created_at"]

    def get_messages(self, obj):
        """
        Custom method to fetch all messages exchanged between the admins and the client.
        """
        user = obj.user
        admins = obj.admins.all()

        messages = Message.objects.filter(
            (models.Q(sender=user) & models.Q(recipient__in=admins))
            | (models.Q(sender__in=admins) & models.Q(recipient=user))
        ).order_by("timestamp")

        return MessageSerializer(messages, many=True).data
