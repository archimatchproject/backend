"""
Module for the OfficeReportArchitect model.

This module defines the OfficeReportArchitect model, which represents reports
filed by offices against architects.
"""

from django.db import models

from app.core.models import BaseModel
from app.moderation import STATUS_CHOICES
from app.moderation.models.Decision import Decision
from app.moderation.models.Reason import Reason
from app.users.models.Architect import Architect
from app.users.models.Office import Office


class OfficeReportArchitect(BaseModel):
    """
    Model for reporting an architect by an office.

    Attributes:
        reported_architect (ForeignKey): The architect being reported.
        reporting_office (ForeignKey): The office submitting the report.
        reasons (ManyToManyField): The reasons associated with the report.
        status (CharField): The current status of the report.
        decision (ForeignKey): The decision taken on the report.
        decision_date (DateTimeField): Date of the final decision.
        comments (TextField): Additional details about the report.
    """

    reported_architect = models.ForeignKey(Architect, on_delete=models.CASCADE, related_name="office_reports")
    reporting_office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="reports_filed")
    reasons = models.ManyToManyField(Reason, related_name="office_reports")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    decision = models.ForeignKey(Decision, on_delete=models.SET_NULL, null=True, blank=True)
    decision_date = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        """
        Meta class for OfficeReportArchitect model.

        Meta Attributes:
            unique_together: Ensures an office cannot report the same architect multiple times.
            verbose_name: Name of the model.
            verbose_name_plural: Plural name of the model.
        """

        unique_together = ("reported_architect", "reporting_office")
        verbose_name = "Office Report on Architect"
        verbose_name_plural = "Office Reports on Architects"

    def __str__(self):
        """
        String representation of the OfficeReportArchitect model.

        Returns:
            str: A string indicating the reported architect and the reporting office.
        """
        return f"Report on {self.reported_architect} by {self.reporting_office}"
