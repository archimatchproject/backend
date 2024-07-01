"""
Module defining the ProjectImage model.

This module contains  ProjectImage classe,
representing different aspects of a project in the application.
"""

from django.core.exceptions import ValidationError
from django.db import models

from app.announcement.models import Announcement


class ProjectImage(models.Model):
    """
    Model representing an image associated with a project.

    Attributes:
        image (ImageField): Image file uploaded for the project, stored in 'images/' directory.
    """

    image = models.ImageField(upload_to="images/ProjectImage/")
    announcement = models.ForeignKey(
        Announcement,
        related_name="project_images",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        """
        Return a string representation of the project image.

        Returns:
            str: String representation of the image.
        """
        return f"Image {self.id} for {self.announcement.id}"

    class Meta:
        """
        Meta class for Project Image model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
