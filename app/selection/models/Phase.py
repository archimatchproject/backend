"""
This module defines the Phase model.

The Phase model represents different stages in the selection process, such as 'Discussion', 'Quotes'
, or 'Decision'.
"""

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.core.models.BaseModel import BaseModel
from app.selection import PHASE_NAME_CHOICES


class Phase(BaseModel):
    """
    Model representing a phase in the selection process.

    Attributes:
        name (CharField): The name of the phase (e.g., 'Discussion', 'Quotes', 'Decision').
        number (PositiveIntegerField): The sequential number of the phase, limited to 1, 2, or 3.
        limit_date (DateField): The date by which the phase should be completed.
        start_date (DateField): The date when the phase starts.
    """

    name = models.CharField(max_length=20, choices=PHASE_NAME_CHOICES, verbose_name=_("Phase Name"))
    number = models.PositiveIntegerField(
        verbose_name=_("Phase Number"),
        help_text=_("The phase number (must be 1, 2, or 3)."),
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        default=1,
    )
    limit_date = models.DateField(
        verbose_name=_("Limit Date"),
        help_text=_("The date by which this phase should be completed."),
    )
    start_date = models.DateField(
        verbose_name=_("Start Date"), help_text=_("The date when the phase starts.")
    )

    class Meta:
        """
        Meta class for the Phase model.
        Attributes:
            verbose_name (str): Human-readable name for the model in singular form.
            verbose_name_plural (str): Human-readable name for the model in plural form.
            ordering (list): Default ordering for the model instances, based on the 'number' field.
        """

        verbose_name = "Phase"
        verbose_name_plural = "Phases"
        ordering = ["number"]

    def __str__(self):
        """
        Returns a string representation of the Phase object.
        The string includes the phase number, name, start date, and limit date.
        Returns:
            str: A formatted string representing the phase.
        """

        return f"""Phase {self.number}: {self.name} (Start: {self.start_date},
                Limit: {self.limit_date})"""
