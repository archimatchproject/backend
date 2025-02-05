"""
Module containing the EventDiscount model and related functionality.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import date


class EventDiscount(models.Model):
    """
    Model representing a discount event like Black Friday or Eid.
    """

    event_name = models.CharField(max_length=255)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def is_active(self):
        """
        Returns True if the discount event is currently active.
        """
        today = date.today()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        """
        String representation of the EventDiscount instance.
        """
        return f"{self.event_name} ({self.discount_percentage}% off)"