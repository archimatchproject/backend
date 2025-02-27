"""
Service module for the Conversation model.

This module defines the service for handling the business logic and exceptions
related to Conversation creation and management.

Classes:
    ConversationService: Service class for Conversation operations.
"""

from django.db import models
from django.db import transaction

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
    def get_client_conversation(cls, request):
        """
        Handles validation and creation of a new Conversation and Message.
            tuple: A tuple containing a boolean indicating success and a string message.
        Raises:
            NotFound: If the admin user is not found.
            APIException: If there is an error with the FCM notification.
        """

        admin_user = ArchimatchUser.objects.filter(is_superuser=True).first()
        if not admin_user:
            raise NotFound(detail="Admin user not found.")
        admin = Admin.objects.get(user=admin_user)

        user = request.user
        # Check if the conversation already exists
        conversation, created = Conversation.objects.get_or_create(user=user)

        # If the conversation was newly created, assign the admin
        if created:
            with transaction.atomic():
                conversation.admins.add(admin)
                conversation.save()

        return True, ConversationSerializer(conversation).data

    @classmethod
    def get_admin_client_conversations(cls, request):
        """
        Retrieves clients who have exchanged messages with the authenticated user.
        params: request
        return: bool, dict
        """
        user = request.user
        admin = Admin.objects.get(user=user)

        # Conversations where the current admin is included
        owned_conversations = Conversation.objects.filter(admins=admin)

        # Conversations that contain only ONE superuser admin
        superuser_conversations = Conversation.objects.filter(admins__user__is_superuser=True).exclude(
            admins__user__is_superuser=False
        )

        # Combine the queries using union to maintain uniqueness
        all_conversations = owned_conversations.union(superuser_conversations)

        # Serialize results
        serializer = ConversationSerializer(all_conversations, many=True)
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

    @classmethod
    def get_conversartion_messages(cls, request):
        """
        Custom method to fetch all messages exchanged between the admins and the users in the conversation.
        """
        recipient_id = request.query_params.get("recipient_id")
        is_admin = request.query_params.get("is_admin", "false").lower() == "true"
        if recipient_id == "":
            return True, []
        if recipient_id is None:
            raise NotFound(detail="client is required")
        conversation = (
            Conversation.objects.filter(user__id=recipient_id if is_admin else request.user.id)
            .prefetch_related("admins__user")
            .first()
        )
        user = conversation.user
        admin_list = conversation.admins.all()
        admin_users = [admin.user for admin in admin_list]
        messages = Message.objects.filter(
            (models.Q(sender=user) & models.Q(recipient__in=admin_users))
            | (models.Q(sender__in=admin_users) & models.Q(recipient=user))
        ).order_by("timestamp")

        return True, MessageSerializer(messages, many=True).data

    @classmethod
    def join_conversation(cls, request):
        """
        Adds the authenticated user to a conversation as an admin if they are not already in it.

        Args:
            cls: The class instance.
            request: The request object containing the conversation ID.

        Raises:
            NotFound: If the conversation ID is not provided or does not exist.

        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        user = request.user
        client_id = request.data.get("client")

        if client_id is None:
            raise NotFound(detail="client is required.")

        admin = Admin.objects.get(user=user)
        conversation = Conversation.objects.get(user_id=client_id)

        # Check if the admin is already in the conversation
        if not conversation.admins.filter(id=admin.id).exists():
            conversation.admins.add(admin)
            return True, "You have been added to the conversation."

        return True, "You are already an admin in this conversation."
