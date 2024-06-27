"""
Module defining the ArchitectSpeciality model.

This module contains the ArchitectSpeciality class, which represents
the specialty of an architect in the application.
"""

from django.db import models

from app.core.models.LabeledIcon import LabeledIcon


class ArchitectSpeciality(LabeledIcon):
    """
    Model representing the specialty of an architect, inheriting from LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.
    """

    class Meta:
        """
        Meta class for Architect Speciality model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Architect Speciality"
        verbose_name_plural = "Architect Specialities"
