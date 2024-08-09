"""
Module for the ArchitectReport model.

This module defines the ArchitectReport model, which represents the reports
filed by clients against architects.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.moderation import STATUS_CHOICES
from app.moderation.models.Decision import Decision
from app.moderation.models.Reason import Reason
from app.users.models.Architect import Architect
from app.users.models.Client import Client


class ArchitectReport(BaseModel):
    """
    Model for reporting an architect.

    Attributes:
        reported_architect (ForeignKey): The architect being reported.
        reporting_client (ForeignKey): The client who is reporting the architect.
        reasons (ManyToManyField): The reasons associated with the report.
    """

    reported_architect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    reporting_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    reasons = models.ManyToManyField(Reason, related_name="reason_architect_reports")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    decision = models.ForeignKey(Decision, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        String representation of the ArchitectReport model.

        Returns:
            str: A string indicating the architect being reported and the client reporting them.
        """
        return f"Report on Architect {self.reported_architect} by {self.reporting_client}"

    class Meta:
        """
        Meta class for ArchitectReport model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        unique_together = ("reported_architect", "reporting_client")
        verbose_name = "Architect Report"
        verbose_name_plural = "Architect Reports"
