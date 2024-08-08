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
from app.messaging.serializers.DeviceSerializer import DeviceSerializer
from app.messaging.serializers.MessageSerializer import MessageSerializer


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
            sender_device = FCMDevice.objects.get(user=user, active=True)
            recipient_device = validated_data.get("recipient_device")
            with transaction.atomic():
                message = Message.objects.create(
                    sender_device=sender_device,
                    recipient_device=recipient_device,
                    content=validated_data.get("content"),
                )
                print(message)
                fcm_message = FCMMessage(
                    notification=Notification(
                        title=f"New Message from {str(user)}", body=validated_data.get("content")
                    )
                )
                recipient_device.send_message(fcm_message)
                return Response(
                    MessageSerializer(message).data,
                    status=status.HTTP_201_CREATED,
                )

        except FCMDevice.DoesNotExist:
            raise NotFound(detail="Device not found or is inactive.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating message: {str(e)}")

    @classmethod
    def get_user_devices(cls, request):
        """
        Retrieves devices associated with the authenticated user.

        Args:
            request (Request): The request object containing the authenticated user.

        Returns:
            Response: A response object containing the list of devices associated with the user.
        """
        user = request.user
        devices = FCMDevice.objects.filter(user=user)
        serialized_devices = DeviceSerializer(devices, many=True)
        return Response(serialized_devices.data)

    @classmethod
    def get_conversation(cls, request):
        """
        Retrieves messages between the authenticated user and a specified device.

        Args:
            request (Request): The request object containing the authenticated user.
            device_id (int): The ID of the device to retrieve messages for.

        Returns:
            Response: A response object containing the list of messages between
            the user and the device.
        """
        user = request.user
        try:
            device_id = request.query_params.get("device_id")
            if not device_id:
                raise serializers.ValidationError(detail="Device ID is required.")
            user_device = FCMDevice.objects.get(user=user, active=True)
            specified_device = FCMDevice.objects.get(id=device_id)
            messages = Message.objects.filter(
                (models.Q(sender_device=user_device) & models.Q(recipient_device=specified_device))
                | (
                    models.Q(sender_device=specified_device)
                    & models.Q(recipient_device=user_device)
                )
            )
            serialized_messages = MessageSerializer(messages, many=True)
            return Response(serialized_messages.data)
        except FCMDevice.DoesNotExist:
            raise NotFound(detail="Device not found.")
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error retrieving conversation: {str(e)}")
