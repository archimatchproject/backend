"""
Module defining the ProjectImage model.

This module contains  ProjectImage classe,
representing different aspects of a project in the application.
"""
from django.core.exceptions import ValidationError
from django.db import models


class ProjectImage(models.Model):
    """
    Model representing an image associated with a project.

    Attributes:
        image (ImageField): Image file uploaded for the project, stored in 'images/' directory.
    """

    image = models.ImageField(upload_to="images/ProjectImage/")

    def clean(self):
        """
        Custom validation to ensure a project's gallery does not exceed 5 images.

        Raises:
            ValidationError: If the project already has 5 images.
        """
        if self.project.images.count() >= 5:
            raise ValidationError("A gallery can contain a maximum of 5 images.")

    def __str__(self):
        """
        Return a string representation of the project image.

        Returns:
            str: String representation of the image.
        """
        return f"Image {self.id} for {self.project.client}"

    class Meta:
        """
        Meta class for Project Image model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
