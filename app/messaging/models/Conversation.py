"""
This module defines the Conversation model for the messaging application.
    Classes:
    - Conversation: Represents a conversation between a list of admins and a specific user.
    Models:
    - Conversation: A Django model that includes fields for user, admins, and created_at.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.users.models.Admin import Admin
from app.users.models.ArchimatchUser import ArchimatchUser


class Conversation(BaseModel):
    """
    Represents a conversation between a list of admins and a specific user.

    Fields:
    - user (ForeignKey): Reference to the specific user in the conversation.
    - admins (ManyToManyField): List of admins participating in the conversation.
    - created_at (DateTimeField): The timestamp when the conversation was created.
    """

    user = models.ForeignKey(ArchimatchUser, related_name="conversations", on_delete=models.CASCADE)
    admins = models.ManyToManyField(Admin, related_name="admin_conversations")

    def __str__(self):
        """
        Returns a string representation of the conversation showing the user and the number of admins involved.

        Returns:
        str: A string in the format 'Conversation with <user> involving <number_of_admins> admins'.
        """
        return f"Conversation with {self.user} involving {self.admins.count()} admins"

    class Meta:
        """
        Meta class for Conversation model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
