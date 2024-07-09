"""
Module containing the ArchitectRequest model.

This module defines the ArchitectRequest model, which includes additional fields and relationships
specific to architects within the Archimatch application.

Classes:
    ArchitectRequest: Defines the ArchitectRequest model with additional fields and relationships.
"""

from datetime import date
from datetime import datetime
from datetime import time

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from rest_framework.serializers import ValidationError

from app.architect_request import ARCHITECT_REQUEST_STATUS_CHOICES
from app.architect_request import TIME_SLOT_CHOICES
from app.core.models import BaseModel
from app.core.models.ArchitectSpeciality import ArchitectSpeciality
from app.core.models.Note import Note
from app.users.models.Admin import Admin


class ArchitectRequest(BaseModel):
    """
    Defines the ArchitectRequest model with additional fields and relationships.

    Fields:
        first_name (CharField): The first name of the architect.
        last_name (CharField): The last name of the architect.
        phone_number (CharField): The phone number of the architect, must be unique.
        address (CharField): The address of the architect.
        architect_identifier (CharField): Identifier code specific to the architect.
        email (EmailField): The email address of the architect.
        architect_speciality (ForeignKey): The specialty of the architect, linked to the
        ArchitectSpeciality model.
        date (DateField): The date of the meeting.
        time_slot (CharField): The time slot of the meeting, selected from predefined
        choices.
    """

    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    phone_number = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255, default="")
    architect_identifier = models.CharField(max_length=10, default="")
    email = models.EmailField(unique=True)

    architect_speciality = models.ForeignKey(
        ArchitectSpeciality,
        on_delete=models.CASCADE,
    )

    date = models.DateField()
    time_slot = models.TimeField(choices=TIME_SLOT_CHOICES)

    meeting_responsable = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=ARCHITECT_REQUEST_STATUS_CHOICES, default="Awaiting Demo"
    )

    notes = GenericRelation(Note)

    def clean(self):
        """
        Custom validation to ensure the time slot is not already taken for the same date.
        """
        conflicting_requests = ArchitectRequest.objects.filter(
            date=self.date, time_slot=self.time_slot
        ).exclude(pk=self.pk)

        if conflicting_requests.exists():
            raise ValidationError("This time slot on the selected date is already taken.")

        now = timezone.now()

        if isinstance(self.date, str):
            try:
                self.date = datetime.strptime(self.date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Date should be in YYYY-MM-DD format.")

        if not isinstance(self.date, date):
            raise ValidationError("Date should be a valid date object.")

        if isinstance(self.time_slot, str):
            try:
                self.time_slot = datetime.strptime(self.time_slot, "%H:%M").time()
            except ValueError:
                raise ValidationError("Time slot should be in HH:MM format.")

        if not isinstance(self.time_slot, time):
            raise ValidationError("Time slot should be a valid time object.")

        meeting_naive_datetime = datetime.combine(self.date, self.time_slot)
        meeting_aware_datetime = timezone.make_aware(
            meeting_naive_datetime,
            timezone.get_current_timezone(),
        )

        if meeting_aware_datetime <= now:
            raise ValidationError("The selected date and time must be in the future.")

    def __str__(self):
        """
        Returns a string representation of the architect request.

        Returns:
            str: The email address and meeting date/time of the architect request.
        """
        return f"{self.email} - Meeting on {self.date} at {self.time_slot.strftime('%H:%M')}"

    class Meta:
        """
        Meta class for ArchitectRequest model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
            unique_together (tuple): Ensures the date and time slot combination is unique.
            ordering (list): Orders the records by date and time_slot.
        """

        verbose_name = "ArchitectRequest"
        verbose_name_plural = "ArchitectRequests"
        unique_together = ("date", "time_slot")
        ordering = ["date", "time_slot"]
