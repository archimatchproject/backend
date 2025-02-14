from django.db import models
from app.users.models.Architect import Architect
from app.announcement.models.Announcement import Announcement
from app.core.models.BaseModel import BaseModel


class ArchitectBox(BaseModel):
    """
    Model representing a collection of announcements for a specific architect.

    Attributes:
        architect (OneToOneField): The architect associated with this box.
        announcements (ManyToManyField): Announcements linked to this architect.
        created_at (DateTimeField): The timestamp when the box was created.
        updated_at (DateTimeField): The timestamp when the box was last updated.
    """

    architect = models.OneToOneField(
        Architect, on_delete=models.CASCADE, related_name="architect_box"
    )
    announcements = models.ManyToManyField(
        Announcement, related_name="architect_boxes", blank=True
    )

    def __str__(self):
        return f"ArchitectBox for {self.architect.user.email}"

    class Meta:
        verbose_name = "Architect Box"
        verbose_name_plural = "Architect Boxes"
