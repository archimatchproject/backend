"""
Module defining the Need model.

This module contains the Need class, which represents a specific need or requirement
in the application, inheriting from the LabeledIcon base class.
"""

from django.db import models

from app.announcement.models.ArchitectSpeciality import ArchitectSpeciality
from app.core.models import LabeledIcon


class Need(LabeledIcon):
    """
    Model representing a specific need or requirement, inheriting from LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.

    Attributes:
        architect_speciality (ForeignKey): Specialization of the architect related to this need.
    """

    architect_speciality = models.ForeignKey(
        ArchitectSpeciality,
        related_name="architect_speciality_needs",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        """
        Meta class for Need model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Need"
        verbose_name_plural = "Needs"
