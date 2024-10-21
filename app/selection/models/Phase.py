"""
This module defines the Phase model.

The Phase model represents different stages in the selection process, such as 'Discussion', 'Quotes', or 'Decision'.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from app.selection import PHASE_NAME_CHOICES

class Phase(models.Model):
    """
    Model representing a phase in the selection process.

    Attributes:
        name (CharField): The name of the phase (e.g., 'Discussion', 'Quotes', 'Decision').
        number (PositiveIntegerField): The sequential number of the phase, limited to 1, 2, or 3.
        limit_date (DateField): The date by which the phase should be completed.
    """
    name = models.CharField(
        max_length=20,
        choices=PHASE_NAME_CHOICES,
        verbose_name=_("Phase Name")
    )
    number = models.PositiveIntegerField(
        verbose_name=_("Phase Number"),
        help_text=_("The phase number (must be 1, 2, or 3)."),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3)
        ],
        default=1
    )
    limit_date = models.DateField(
        verbose_name=_("Limit Date"),
        help_text=_("The date by which this phase should be completed.")
    )

    class Meta:
        verbose_name = "Phase"
        verbose_name_plural = "Phases"
        ordering = ['number']

    def __str__(self):
        return f"Phase {self.number}: {self.name} (Limit: {self.limit_date})"
