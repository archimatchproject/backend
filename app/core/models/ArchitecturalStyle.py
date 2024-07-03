"""
Module defining the ArchitecturalStyle model.

This module contains the ArchitecturalStyle class, which represents
the specialty of an architect in the application.
"""

from django.db import models


class ArchitecturalStyle(models.Model):
    """
    Model representing architectural styles.

    label
    icon
    """

    label = models.CharField(max_length=255, default="")
    icon = models.ImageField(upload_to="ArchitecturalStyleIcons/")

    def __str__(self):
        """
        Return a string representation of the architectural style.

        Returns:
            str: String representation of the architectural style, including its ID and associated
            client.
        """
        return self.label

    class Meta:
        """
        Meta class for ArchitecturalStyle model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Architectural Style"
        verbose_name_plural = "Architectural Styles"
