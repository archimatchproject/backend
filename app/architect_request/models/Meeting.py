"""
Module containing the Meeting model.

This module defines the Meeting model, which includes additional fields and relationships
specific to architects within the Archimatch application.

Classes:
    Meeting: Defines the Meeting model with additional fields and relationships.
"""
import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from app.architect_request import TIME_SLOT_CHOICES


class Meeting(models.Model):
    """
    Defines the Meeting model with date and time slots.

    Fields:
        date (DateField): The date of the meeting.
        time_slot (CharField): The time slot of the meeting, selected from predefined choices.
    """

    date = models.DateField()
    time_slot = models.TimeField(choices=TIME_SLOT_CHOICES)

    def clean(self):
        """
        Custom validation to ensure the time slot is not already taken for the same date.
        """
        if Meeting.objects.filter(date=self.date, time_slot=self.time_slot).exists():
            raise ValidationError(
                "This time slot on the selected date is already taken."
            )

        now = timezone.now()
        meeting_naive_datetime = datetime.datetime.combine(self.date, self.time_slot)
        meeting_aware_datetime = timezone.make_aware(
            meeting_naive_datetime, timezone.get_current_timezone()
        )

        if meeting_aware_datetime <= now:
            raise ValidationError("The selected date and time must be in the future.")

    def __str__(self):
        """
        Returns the string representation of the meeting as date and time slot.

        Returns:
            str: The date and time slot of the meeting.
        """
        return f"{self.date} at {self.time_slot.strftime('%H:%M')}"

    class Meta:
        """
        Meta class for Meeting model.

        Meta Attributes:
            unique_together (tuple): Ensures the date and time slot combination is unique.
            ordering (list): Orders the meetings by date and time_slot.
        """

        unique_together = ("date", "time_slot")
        ordering = ["date", "time_slot"]
