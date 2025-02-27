"""
This module defines the Meeting model, which is used to manage scheduled meetings
within the application. The model includes fields for attendee information, scheduling
details, and the status of the meeting.
"""

from django.db import models

from app.users import MEETING_STATUS_CHOICES
from app.users import PENDING


class Meeting(models.Model):
    """
    The Meeting model stores information about scheduled meetings. This includes
    the attendee's first and last names, contact information, the meeting time, and
    the status of the meeting. It also associates each meeting with an admin and a
    specific time slot.
    """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    admin = models.ForeignKey("users.Admin", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.ForeignKey("users.TimeSlot", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=MEETING_STATUS_CHOICES, default=PENDING)

    def __str__(self):
        """
        Returns a string representation of the Meeting object.
        The string includes the first name, last name, date, and time of the meeting.
        Returns:
            str: A formatted string describing the meeting.
        """

        return f"Meeting with {self.first_name} {self.last_name} on {self.date} at {self.time}"

    class Meta:
        """
        Meta class to define metadata for the Meeting model.
        Attributes:
            verbose_name (str): Human-readable name for the model in singular form.
            verbose_name_plural (str): Human-readable name for the model in plural form.
        """

        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"
