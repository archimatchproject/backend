"""
Module defining the RealizationImage model.

This module contains  RealizationImage class,
representing different aspects of a project in the application.
"""

from django.db import models

from app.architect_realization.models.Realization import Realization


class RealizationImage(models.Model):
    """
    Model representing an image associated with a realization.

    Attributes:
        image (ImageField): Image file uploaded for the project, stored in 'images/' directory.
    """

    image = models.ImageField(upload_to="images/RealizationImage/")
    realization = models.ForeignKey(
        Realization,
        related_name="realization_images",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        """
        Return a string representation of the project image.

        Returns:
            str: String representation of the image.
        """
        return f"Image {self.id} for {self.realization.id}"

    class Meta:
        """
        Meta class for Project Image model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
