"""
This module defines the SelectionSettings model, a singleton model for managing configuration settings
related to the selection process, such as phase durations, communication timing, and project management constraints.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class SelectionSettings(models.Model):
    """
    Singleton model for managing configuration settings related to selections.

    Attributes:
        phase_days (PositiveIntegerField): Number of days for each phase in the selection process.
        days_before_call_email (PositiveIntegerField): Number of days to send an email before making a phone call.
        days_to_phone_call (PositiveIntegerField): Number of days within which a phone call should be made.
        days_after_call_email (PositiveIntegerField): Number of days to send an email after the phone call.
        days_to_rediffuse (PositiveIntegerField): Number of days to re-publish the project.
        days_to_lock_project (PositiveIntegerField): Number of days after which the project is locked.
        times_to_unlock_project (PositiveIntegerField): Number of times the project can be unlocked.
        days_for_admin_management (PositiveIntegerField): Number of days for the admin to manage the selection.
        email_sending_hour (TimeField): Hour of the day for sending email notifications.
    """

    phase_days = models.PositiveIntegerField(
        verbose_name=_("Phase Number of Days"),
        help_text=_("The number of days for each phase in the selection process.")
    )
    days_before_call_email = models.PositiveIntegerField(
        verbose_name=_("Days Before Call Email"),
        help_text=_("The number of days to send an email before making a phone call.")
    )
    days_to_phone_call = models.PositiveIntegerField(
        verbose_name=_("Days to Phone Call"),
        help_text=_("The number of days within which a phone call should be made.")
    )
    days_after_call_email = models.PositiveIntegerField(
        verbose_name=_("Days After Call Email"),
        help_text=_("The number of days to send an email after the phone call.")
    )
    days_to_rediffuse = models.PositiveIntegerField(
        verbose_name=_("Days to Rediffuse"),
        help_text=_("The number of days to re-publish the project.")
    )
    days_to_lock_project = models.PositiveIntegerField(
        verbose_name=_("Days to Lock Project"),
        help_text=_("The number of days after which the project is locked.")
    )
    times_to_unlock_project = models.PositiveIntegerField(
        verbose_name=_("Times to Unlock Project"),
        help_text=_("The number of times the project can be unlocked.")
    )
    days_for_admin_management = models.PositiveIntegerField(
        verbose_name=_("Days for Admin Management"),
        help_text=_("The number of days for the admin to manage the selection.")
    )
    email_sending_hour = models.TimeField(
        verbose_name=_("Email Sending Hour"),
        help_text=_("The hour of the day for sending email notifications.")
    )

    class Meta:
        verbose_name = "Selection Settings"
        verbose_name_plural = "Selection Settings"

    def clean(self):
        """
        Enforce the singleton behavior by checking if another instance exists before saving.
        """
        if SelectionSettings.objects.exists() and not self.pk:
            raise ValidationError("Only one instance of SelectionSettings is allowed.")

    def save(self, *args, **kwargs):
        """
        Override save to ensure only one instance of the model exists.
        """
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return "Selection Settings"
