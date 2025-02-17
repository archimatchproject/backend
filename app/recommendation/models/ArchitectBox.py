"""
Model representing a collection of announcements for a specific architect.

Attributes:
    architect (OneToOneField): The architect associated with this box.
    announcements (ManyToManyField): Announcements linked to this architect.
    created_at (DateTimeField): The timestamp when the box was created.
    updated_at (DateTimeField): The timestamp when the box was last updated.
"""

from django.db import models

from app.announcement.models.Announcement import Announcement
from app.core.models.BaseModel import BaseModel
from app.users.models.Architect import Architect


class ArchitectBox(BaseModel):
    """
    Model representing a collection of announcements for a specific architect.

    Attributes:
        architect (OneToOneField): The architect associated with this box.
        announcements (ManyToManyField): Announcements linked to this architect.
        created_at (DateTimeField): The timestamp when the box was created.
        updated_at (DateTimeField): The timestamp when the box was last updated.
    """

    architect = models.OneToOneField(Architect, on_delete=models.CASCADE, related_name="architect_box")
    announcements = models.ManyToManyField(Announcement, related_name="architect_boxes", blank=True)

    def __str__(self):
        """
        Returns a string representation of the ArchitectBox instance.
        Returns:
            str: A string in the format "ArchitectBox for {email}" where {email} is the email of the associated
            architect's user.
        """

        return f"ArchitectBox for {self.architect.user.email}"

    class Meta:
        """
        Meta class for defining model metadata.
        Attributes:
            verbose_name (str): Human-readable singular name for the model.
            verbose_name_plural (str): Human-readable plural name for the model.
        """

        verbose_name = "Architect Box"
        verbose_name_plural = "Architect Boxes"
