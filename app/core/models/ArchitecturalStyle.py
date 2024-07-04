"""
Module defining the ArchitecturalStyle model.

This module contains the ArchitecturalStyle class, which represents
the specialty of an architect in the application.
"""

from django.db import models

from app.core.models.LabeledIcon import LabeledIcon


class ArchitecturalStyle(LabeledIcon):
    """
    Model representing architectural styles.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.
    """

    icon = models.ImageField(upload_to="ArchitecturalStyleIcons/")

    class Meta:
        """
        Meta class for ArchitecturalStyle model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Architectural Style"
        verbose_name_plural = "Architectural Styles"

    def __str__(self):
        """
        Return a string representation of the architectural style.

        Returns:
            str: String representation of the architectural style, including its ID and associated
            client.
        """
        return self.label
