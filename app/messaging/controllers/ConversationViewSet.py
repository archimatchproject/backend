"""
ViewSet module for the Conversation model.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.messaging.models.Conversation import Conversation
from app.messaging.serializers.ConversationSerializer import ConversationSerializer
from app.messaging.services.ConversationService import ConversationService


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Message model.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the create method to use MessageService for handling the creation
        of a new message.
        """
        return ConversationService.create_conversation(request)

    @action(detail=False, methods=["GET"], url_path="conversation")
    @handle_service_exceptions
    def get_admin_client_messages(self, request):
        """
        Retrieve all messages between the authenticated user and a specified device.

        Args:
            request (Request): The request object containing the device ID.

        Returns:
            Response: A serialized response containing the list of messages.
        """

        success, data = ConversationService.get_admin_client_conversations(request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="add-admin")
    @handle_service_exceptions
    def add_admin_to_conversation(self, request):
        """
        Adds an admin to a conversation.

        Args:
            request (Request): The request object containing the admin and conversation IDs.

        Returns:
            Response: A response indicating success or failure.
        """
        success, message = ConversationService.add_admin_to_conversation(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="remove-admin")
    @handle_service_exceptions
    def remove_admin_from_conversation(self, request):
        """
        Removes an admin from a conversation.

        Args:
            request (Request): The request object containing the admin and conversation IDs.

        Returns:
            Response: A response indicating success or failure.
        """
        success, message = ConversationService.remove_admin_from_conversation(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="add-self")
    @handle_service_exceptions
    def add_self_to_conversation(self, request):
        """
        Adds the authenticated user to a conversation as an admin.

        Args:
            request (Request): The request object containing the conversation ID.

        Returns:
            Response: A response indicating success or failure.
        """
        success, message = ConversationService.add_self_to_conversation(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="remove-self")
    @handle_service_exceptions
    def remove_self_from_conversation(self, request):
        """
        Removes the authenticated user from a conversation as an admin.

        Args:
            request (Request): The request object containing the conversation ID.

        Returns:
            Response: A response indicating success or failure.
        """
        success, message = ConversationService.remove_self_from_conversation(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)
