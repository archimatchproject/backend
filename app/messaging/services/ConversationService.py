"""
Service module for the Conversation model.

This module defines the service for handling the business logic and exceptions
related to Conversation creation and management.

Classes:
    ConversationService: Service class for Conversation operations.
"""

from django.db import models
from django.db import transaction

from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message as FCMMessage
from firebase_admin.messaging import Notification
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound

from app.messaging.models.Conversation import Conversation
from app.messaging.models.Message import Message
from app.messaging.serializers.ConversationSerializer import ConversationSerializer
from app.messaging.serializers.MessageSerializer import MessageSerializer
from app.users.models.Admin import Admin
from app.users.models.ArchimatchUser import ArchimatchUser


class ConversationService:
    """
    Service class for handling Conversation operations.

    Handles business logic and exception handling for Conversation creation and management.


    """

    @classmethod
    def create_conversation(cls, request):
        """
        Handles validation and creation of a new Conversation and Message.
            tuple: A tuple containing a boolean indicating success and a string message.
        Raises:
            NotFound: If the admin user is not found.
            APIException: If there is an error with the FCM notification.
        """
        data = request.data
        admin_user = ArchimatchUser.objects.filter(is_superuser=True).first()
        if not admin_user:
            raise NotFound(detail="Admin user not found.")
        admin = Admin.objects.get(user=admin_user)
        data.update({"recipient_id": admin.user.id})
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = request.user

        # Fetch the recipient user based on provided data
        recipient = validated_data.get("recipient_id")

        # Begin transaction to save the message
        with transaction.atomic():
            Message.objects.create(
                sender=user,
                recipient=recipient,
                content=validated_data.get("content"),
            )

            # Send notification to recipient’s device (if required)
            recipient_device = FCMDevice.objects.filter(user=recipient, active=True).first()
            if recipient_device:
                fcm_message = FCMMessage(
                    data={"user_id": str(user.id)},
                    notification=Notification(
                        title=f"New Message from {str(user)}",
                        body=validated_data.get("content"),
                    ),
                    token=recipient_device.registration_id,
                )
                try:
                    recipient_device.send_message(fcm_message)
                except Exception as fcm_error:
                    raise APIException(detail="Error with FCM notification: " + str(fcm_error))
            conversation = Conversation.objects.create(user=user)
            conversation.admins.add(admin)
            conversation.save()
            return True, "conversation added"

    @classmethod
    def get_admin_client_conversations(cls, request):
        """
        Retrieves clients who have exchanged messages with the authenticated user.
        params: request
        return: bool, dict
        """
        user = request.user
        admin = Admin.objects.get(user=user)
        owned_conversations = Conversation.objects.filter(admins=admin)

        superuser_conversations = (
            Conversation.objects.filter(admins__user__is_superuser=True)
            .annotate(num_superusers=models.Count("admins", filter=models.Q(admins__user__is_superuser=True)))
            .filter(num_superusers=1)
        )
        owned_conversations = owned_conversations | superuser_conversations
        serializer = ConversationSerializer(owned_conversations, many=True)
        return True, serializer.data

    @classmethod
    def add_admin_to_conversation(cls, request):
        """
        Adds an admin to a conversation.
        Args:
            cls: The class instance.
            request: The request object containing the admin and conversation IDs.
        Raises:
            NotFound: If the conversation ID or admin ID is not provided or does not exist.
        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        admin_id = request.data.get("admin")
        conversation_id = request.data.get("conversation")

        if conversation_id is None:
            raise NotFound(detail="Conversation is required.")
        if admin_id is None:
            raise NotFound(detail="Admin is required.")

        admin = Admin.objects.get(id=admin_id)
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.admins.add(admin)

        return True, "admin added to conversation"

    @classmethod
    def remove_admin_from_conversation(cls, request):
        """
        Removes an admin from a conversation.
        Args:
            cls: The class instance.
            request: The request object containing the admin and conversation IDs.
        Raises:
            NotFound: If the conversation ID or admin ID is not provided or does not exist.
        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        admin_id = request.data.get("admin")
        conversation_id = request.data.get("conversation")

        if conversation_id is None:
            raise NotFound(detail="Conversation is required.")
        if admin_id is None:
            raise NotFound(detail="Admin is required.")

        admin = Admin.objects.get(id=admin_id)
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.admins.remove(admin)

        return True, "admin removed from conversation"

    @classmethod
    def add_self_to_conversation(cls, request):
        """
        Adds the authenticated user to a conversation as an admin.
        Args:
            cls: The class instance.
            request: The request object containing the conversation ID.
        Raises:
            NotFound: If the conversation ID is not provided or does not exist.
        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        user = request.user
        conversation_id = request.data.get("conversation")

        if conversation_id is None:
            raise NotFound(detail="Conversation is required.")

        admin = Admin.objects.get(user=user)
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.admins.add(admin)

        return True, "You have been added to the conversation"

    @classmethod
    def remove_self_from_conversation(cls, request):
        """
        Removes the authenticated user from a conversation as an admin.
        Args:
            cls: The class instance.
            request: The request object containing the conversation ID.
        Raises:
            NotFound: If the conversation ID is not provided or does not exist.
        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        user = request.user
        conversation_id = request.data.get("conversation")

        if conversation_id is None:
            raise NotFound(detail="Conversation is required.")

        admin = Admin.objects.get(user=user)
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.admins.remove(admin)

        return True, "You have been removed from the conversation"
