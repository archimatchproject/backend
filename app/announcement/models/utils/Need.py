from django.db import models

from .ArchitectSpeciality import ArchitectSpeciality
from .LabeledIcon import LabeledIcon


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
        related_name="needs",
        on_delete=models.CASCADE,
        default=None,
    )
