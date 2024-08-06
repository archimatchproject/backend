"""
Module for the Reason model.

This module defines the Reason model, which represents the reasons
for reporting various entities within the application.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.moderation import REPORT_TYPES


class Reason(BaseModel):
    """
    Model representing a reason for reporting.

    Attributes:
        name (CharField): The name or description of the reason.
        report_type (CharField): The type of report this reason applies to.
    """

    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, default=REPORT_TYPES[0][0])

    def __str__(self):
        """
        String representation of the Reason model.

        Returns:
            str: The name of the reason.
        """
        return self.name

    class Meta:
        """
        Meta class for Reason model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Reason"
        verbose_name_plural = "Reasons"
