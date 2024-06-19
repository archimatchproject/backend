from django.db import models

from app.announcement.models.ArchitectSpeciality import ArchitectSpeciality
from app.announcement.models.LabeledIcon import LabeledIcon


class Need(LabeledIcon):
    """
    Model representing a specific need or requirement, inheriting from LabeledIcon.

    Inherits:
        LabeledIcon: Base class providing fields for label and icon.

    Attributes:
        architect_speciality (ForeignKey): Specialization of the architect related to this need.
    """

    architect_speciality = models.ForeignKey(
        ArchitectSpeciality, related_name="needs", on_delete=models.CASCADE, null=True
    )

    class Meta:
        """Meta class for Need model."""

        verbose_name = "Need"
        verbose_name_plural = "Needs"
