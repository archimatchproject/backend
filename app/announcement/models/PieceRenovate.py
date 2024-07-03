"""
Module defining the PieceRenovate model.

This module contains the PieceRenovate class, which represents a piece or area
to be renovated in the application, inheriting from the LabeledIcon base class.
"""

from app.core.models import LabeledIcon


class PieceRenovate(LabeledIcon):
    """
    Model representing a piece or area to be renovated, inheriting from LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.
    """

    class Meta:
        """
        Meta class for Piece Renovate model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Piece Renovate"
        verbose_name_plural = "Piece Renovates"
