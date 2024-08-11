"""
This module defines the models for storing messages exchanged between devices using Firebase
 Cloud Messaging (FCM).
"""

from django.db import models

from fcm_django.models import FCMDevice


class Message(models.Model):
    """
    Represents a message exchanged between two devices using Firebase Cloud Messaging (FCM).

    Fields:
    - sender_device (ForeignKey): Reference to the FCM device that sends the message.
    - recipient_device (ForeignKey): Reference to the FCM device that receives the message.
    - content (TextField): The content of the message.
    - timestamp (DateTimeField): The timestamp when the message was sent.
    """

    sender_device = models.ForeignKey(
        FCMDevice, related_name="sent_messages", on_delete=models.CASCADE
    )
    recipient_device = models.ForeignKey(
        FCMDevice, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the message, showing sender and recipient.

        Returns:
        str: A string in the format 'Message from <sender_device> to <recipient_device>'.
        """
        return f"Message from {self.sender_device} to {self.recipient_device}"

    class Meta:
        """
        Meta class for Message model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Message"
        verbose_name_plural = "Messages"
