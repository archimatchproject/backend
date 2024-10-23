"""
This module defines the Note model.

The Note model is used to store notes that can be associated with various other models
using a generic foreign key.
"""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from app.core.models.BaseModel import BaseModel


class Note(BaseModel):
    """
    Note model for storing text messages with a generic foreign key.

    Attributes:
        message (TextField): The content of the note.
        created_at (DateTimeField): The date and time when the note was created.
        content_type (ForeignKey): The type of the related object.
        object_id (PositiveIntegerField): The ID of the related object.
        content_object (GenericForeignKey): The related object.
    """

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic Foreign Key fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        """
        Returns a string representation of the Note instance.

        The representation includes the first 20 characters of the message
        and the associated content object.

        Returns:
            str: A string representation of the Note instance.
        """
        return f"Note: {self.message[:20]} (on {self.content_object})"

    class Meta:
        """
        Meta class for the Note model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Note"
        verbose_name_plural = "Notes"
