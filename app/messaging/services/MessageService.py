"""
Service module for the Message model.

This module defines the service for handling the business logic and exceptions
related to Message creation and management.

Classes:
    MessageService: Service class for Message operations.
"""

from django.db import models
from django.db import transaction

from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message as FCMMessage
from firebase_admin.messaging import Notification
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.messaging.models.Message import Message
from app.messaging.serializers.MessageSerializer import MessageSerializer
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.serializers.ArchimatchUserSerializer import ArchimatchUserSerializer


class MessageService:
    """
    Service class for handling Message operations.

    Handles business logic and exception handling for Message creation and management.

    Methods:
        create_message(request): Handles validation and creation of a new Message.
        get_device_messages(request, device_id): Retrieves messages related to a specific device.
    """

    @classmethod
    def create_message(cls, request):
        """
        Handles validation and creation of a new Message.

        Args:
            request (Request): The request object containing the authenticated user
            and message data.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = request.user

        try:
            # Fetch the recipient user based on provided data
            recipient = validated_data.get("recipient_id")

            # Begin transaction to save the message
            with transaction.atomic():
                message = Message.objects.create(
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
                        print(f"Error sending FCM message: {fcm_error}")
                        raise APIException(detail="Error with FCM notification: " + str(fcm_error))

                return Response(
                    MessageSerializer(message).data,
                    status=status.HTTP_201_CREATED,
                )

        except ArchimatchUser.DoesNotExist:
            raise NotFound(detail="Recipient user not found.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating message: {str(e)}")

    @classmethod
    def get_user_contacts(cls, request):
        """
        Retrieves users with whom the authenticated user has exchanged messages.

        Args:
            request (Request): The request object containing the authenticated user.

        Returns:
            Response: A response object containing the list of users the authenticated user
                    has sent or received messages from.
        """
        user = request.user

        # Get users who are either recipients of messages from the user or senders of messages
        # to the user
        sent_users = ArchimatchUser.objects.filter(received_messages__sender=user)
        received_users = ArchimatchUser.objects.filter(sent_messages__recipient=user)

        # Combine the querysets and remove duplicates
        contacts = (sent_users | received_users).distinct()

        # Serialize the user contacts
        serialized_users = ArchimatchUserSerializer(
            contacts, many=True
        )  # Replace UserSerializer with your actual serializer for users
        return Response(serialized_users.data)

    @classmethod
    def get_conversation(cls, request):
        """
        Retrieves messages between the authenticated user and a specified user.

        Args:
            request (Request): The request object containing the authenticated user.

        Returns:
            Response: A response object containing the list of messages between
            the user and the specified recipient.
        """
        user = request.user
        try:
            recipient_id = request.query_params.get("recipient_id")
            if not recipient_id:
                raise serializers.ValidationError(detail="Recipient ID is required.")

            recipient = ArchimatchUser.objects.get(id=recipient_id)
            messages = Message.objects.filter(
                (models.Q(sender=user) & models.Q(recipient=recipient))
                | (models.Q(sender=recipient) & models.Q(recipient=user))
            ).order_by("timestamp")

            serialized_messages = MessageSerializer(messages, many=True)
            return Response(serialized_messages.data)

        except ArchimatchUser.DoesNotExist:
            raise NotFound(detail="Recipient user not found.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error retrieving conversation: {str(e)}")
