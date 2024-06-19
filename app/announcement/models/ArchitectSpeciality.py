from django.db import models

from app.announcement.models.LabeledIcon import LabeledIcon


class ArchitectSpeciality(LabeledIcon):
    """
    Model representing the specialty of an architect, inheriting from LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.

    This class inherits all fields and behavior from LabeledIcon.
    """

    pass

    class Meta:
        """Meta class for Architect Speciality model."""

        verbose_name = "Architect Speciality"
        verbose_name_plural = "Architect Specialities"
