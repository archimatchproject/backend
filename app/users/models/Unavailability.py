from django.db import models
from app.architect_request import TIME_SLOT_CHOICES
from app.core.models import BaseModel
from app.users.models.TimeSlot import TimeSlot

TIME_SLOT_MAP = {label: time for time, label in TIME_SLOT_CHOICES}

class Unavailability(BaseModel):
    """
    Model representing the unavailability of an admin on specific dates and times.
    
    Attributes:
        admin (ForeignKey): The admin user who has this unavailability.
        date (DateField): The date of the unavailability.
        time_slots (ManyToManyField): The specific time slots during which the admin is unavailable.
        whole_day (BooleanField): Indicates whether the admin is unavailable for the entire day.
    """
    admin = models.ForeignKey("users.Admin", on_delete=models.CASCADE, related_name="unavailabilities")
    date = models.DateField()
    time_slots = models.ManyToManyField(TimeSlot, blank=True)
    whole_day = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Unavailability"
        verbose_name_plural = "Unavailabilities"

    def __str__(self):
        return f"{self.admin.user.email} - {self.date}"
