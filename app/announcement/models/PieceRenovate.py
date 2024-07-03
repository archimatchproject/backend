"""
Module defining the PieceRenovate model.

This module contains the PieceRenovate class, which represents a piece or area
to be renovated in the application.
"""

from django.db import models

from app.core.models.PropertyType import PropertyType


class PieceRenovate(models.Model):
    """
    Model representing a piece or area to be renovated.

    label
    icon
    """

    label = models.CharField(max_length=255, default="")
    icon = models.ImageField(upload_to="PieceRenovateIcons/")
    property_type = models.ForeignKey(
        PropertyType,
        related_name="property_type_renovation_pieces",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        """
        Return a string representation of the labeled icon.

        Returns:
            str: Label or name associated with the icon.
        """
        return self.label

    class Meta:
        """
        Meta class for Piece Renovate model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Piece Renovate"
        verbose_name_plural = "Piece Renovates"
