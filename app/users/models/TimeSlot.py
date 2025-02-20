"""
TimeSlot model
This module defines the TimeSlot model, which represents a specific time slot in a day.
It includes the following attributes:
Attributes:
    time (TimeField): A unique field representing the time slot, with choices defined in TIME_SLOT_CHOICES.
Methods:
    __str__(): Returns the display value of the time slot.
Dependencies:
    - django.db.models
    - app.architect_request.TIME_SLOT_CHOICES
    - app.core.models.BaseModel
"""

from django.db import models

from app.architect_request import TIME_SLOT_CHOICES
from app.core.models import BaseModel


class TimeSlot(BaseModel):
    """
    Model representing a specific time slot in a day.
    """

    time = models.TimeField(unique=True, choices=TIME_SLOT_CHOICES)

    def __str__(self):
        """
        Returns a string representation of the TimeSlot instance.
        This method overrides the default string representation of the object
        to return the display value of the time slot.
        Returns:
            str: The display value of the time slot.
        """

        return self.get_time_display()
