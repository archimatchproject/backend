"""
Module for the ReviewReport model.

This module defines the ReviewReport model, which represents the reports
filed by architects against client reviews.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.moderation import STATUS_CHOICES
from app.moderation.models.ClientReview import ClientReview
from app.moderation.models.Decision import Decision
from app.moderation.models.Reason import Reason
from app.users.models.Architect import Architect


class ReviewReport(BaseModel):
    """
    Model for reporting a review.

    Attributes:
        reported_review (ForeignKey): The review being reported.
        reporting_architect (ForeignKey): The architect who is reporting the review.
        reasons (ManyToManyField): The reasons associated with the report.
    """

    reported_review = models.ForeignKey(ClientReview, on_delete=models.SET_NULL, null=True)
    reporting_architect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    reasons = models.ManyToManyField(Reason, related_name="reason_review_reports")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    decision = models.ForeignKey(Decision, on_delete=models.SET_NULL, null=True, blank=True)
    decision_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        String representation of the ReviewReport model.

        Returns:
            str: A string indicating the review being reported and the architect reporting it.
        """
        return f"Report on Review {self.reported_review} by {self.reporting_architect}"

    class Meta:
        """
        Meta class for ReviewReport model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        unique_together = ("reporting_architect", "reported_review")
        verbose_name = "Review Report"
        verbose_name_plural = "Review Reports"
