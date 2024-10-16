"""
ViewSet module for the Message model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.messaging.models.Message import Message
from app.messaging.serializers.MessageSerializer import MessageSerializer
from app.messaging.services.MessageService import MessageService


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Message model.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["create", "user_devices", "conversation"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Override the create method to use MessageService for handling the creation
        of a new message.
        """
        return MessageService.create_message(request)

    @action(detail=False, methods=["GET"], url_path="user-devices")
    def user_devices(self, request):
        """
        Retrieve all devices associated with the authenticated user.

        Returns:
            Response: A serialized response containing the list of devices.
        """
        return MessageService.get_user_devices(request)

    @action(detail=False, methods=["GET"], url_path="conversation")
    def conversation(self, request):
        """
        Retrieve all messages between the authenticated user and a specified device.

        Args:
            request (Request): The request object containing the device ID.

        Returns:
            Response: A serialized response containing the list of messages.
        """

        return MessageService.get_conversation(request)
