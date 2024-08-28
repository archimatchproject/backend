from django.db import models
from app.core.models import BaseModel
from app.architect_request import TIME_SLOT_CHOICES

class TimeSlot(BaseModel):
    """
    Model representing a specific time slot in a day.
    """
    time = models.TimeField(unique=True,choices=TIME_SLOT_CHOICES)
    
    def __str__(self):
        return self.get_time_display() 