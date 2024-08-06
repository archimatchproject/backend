"""
Module for the ProjectReport model.

This module defines the ProjectReport model, which represents the reports
filed by architects against projects.
"""

from django.db import models

from app.announcement.models import Announcement
from app.core.models.BaseModel import BaseModel
from app.moderation import STATUS_CHOICES
from app.moderation.models.Decision import Decision
from app.moderation.models.Reason import Reason
from app.users.models import Architect


class ProjectReport(BaseModel):
    """
    Model for reporting a project.

    Attributes:
        reported_project (ForeignKey): The project being reported.
        reporting_architect (ForeignKey): The architect who is reporting the project.
        reasons (ManyToManyField): The reasons associated with the report.
    """

    reported_project = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    reporting_architect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    reasons = models.ManyToManyField(Reason, related_name="reason_project_reports")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    decision = models.ForeignKey(Decision, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        String representation of the ProjectReport model.

        Returns:
            str: A string indicating the project being reported and the architect reporting it.
        """
        return f"Report on Project {self.reported_project} by {self.reporting_architect}"

    class Meta:
        """
        Meta class for ProjectReport model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        unique_together = ("reporting_architect", "reported_project")
        verbose_name = "Project Report"
        verbose_name_plural = "Project Reports"
