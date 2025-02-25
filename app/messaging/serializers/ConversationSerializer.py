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
    Serializer for the Conversation model, including admins, user, messages, last admin, and last message.
    """

    user = ArchimatchUserSerializer()
    admins = AdminSerializer(many=True)
    messages = serializers.SerializerMethodField()
    last_admin = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the ConversationSerializer.
        Attributes:
            model (type): The model that is being serialized, in this case, Conversation.
            fields (list): A list of fields to be included in the serialized output.
                           Includes "user", "admins", "messages", "last_admin", "last_message", and "created_at".
        """

        model = Conversation
        fields = [
            "user",
            "admins",
            "messages",
            "last_admin",
            "last_message",
            "created_at",
        ]

    def get_messages(self, obj):
        """
        Custom method to fetch all messages exchanged between the admins and the users in the conversation.
        """
        user = obj.user
        admins = obj.admins.all()

        admin_users = [admin.user for admin in admins]

        messages = Message.objects.filter(
            (models.Q(sender=user) & models.Q(recipient__in=admin_users))
            | (models.Q(sender__in=admin_users) & models.Q(recipient=user))
        ).order_by("timestamp")

        return MessageSerializer(messages, many=True).data

    def get_last_admin(self, obj):
        """
        Custom method to return the last admin in the admins list.
        """
        last_admin = obj.admins.last()  # Gets the last admin in the queryset
        return AdminSerializer(last_admin).data if last_admin else None

    def get_last_message(self, obj):
        """
        Custom method to return the last message exchanged in the conversation.
        """
        user = obj.user
        admins = obj.admins.all()
        admin_users = [admin.user for admin in admins]

        last_message = (
            Message.objects.filter(
                (models.Q(sender=user) & models.Q(recipient__in=admin_users))
                | (models.Q(sender__in=admin_users) & models.Q(recipient=user))
            )
            .order_by("-timestamp")
            .first()
        )  # Get the most recent message

        return MessageSerializer(last_message).data if last_message else None
