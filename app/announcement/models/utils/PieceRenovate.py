from django.db import models

from .LabeledIcon import LabeledIcon


class PieceRenovate(LabeledIcon):
    """
    Model representing a piece or area to be renovated, inheriting from LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.

    Attributes:
        number (PositiveSmallIntegerField): Number representing the piece to be renovated, default is 0.
    """

    number = models.PositiveSmallIntegerField(default=0)
