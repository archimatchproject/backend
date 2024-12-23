"""
This module defines the SelectionReport model, which represents a report for a selection.

Classes:
    SelectionReport: A Django model representing a report for a selection.

Usage:
    This model is used to create and manage reports for selections in the application.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.moderation import STATUS_CHOICES
from app.moderation.models.Decision import Decision
from app.moderation.models.Reason import Reason
from app.users.models.Client import Client
from app.selection.models.Selection import Selection


class SelectionReport(BaseModel):
    """
    Model for reporting an selection.

    Attributes:
        reported_architect (ForeignKey): The architect being reported.
        reporting_client (ForeignKey): The client who is reporting the architect.
        reasons (ManyToManyField): The reasons associated with the report.
    """

    selection = models.ForeignKey(Selection, on_delete=models.CASCADE)
    reporting_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    reasons = models.ManyToManyField(Reason, related_name="reason_selections_reports")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    decision = models.ForeignKey(
        Decision, on_delete=models.SET_NULL, null=True, blank=True
    )
    decision_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        String representation of the ArchitectReport model.

        Returns:
            str: A string indicating the architect being reported and the client reporting them.
        """
        return f"Report on Architect {self.selection} by {self.reporting_client}"

    class Meta:
        """
        Meta class for ArchitectReport model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        unique_together = ("selection", "reporting_client")
        verbose_name = "Selection Report"
        verbose_name_plural = "Selection Reports"
