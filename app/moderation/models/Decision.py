"""
Module for the Decision model.

This module defines the Decision model, which represents the decisions
for reporting various entities within the application.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.moderation import REPORT_TYPES


class Decision(BaseModel):
    """
    Model representing a decision related to a report.

    Attributes:
        name (CharField): The name or description of the decision.
        report_type (CharField): The type of report this decision applies to.
    """

    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, default=REPORT_TYPES[0][0])

    def __str__(self):
        """
        String representation of the Decision model.

        Returns:
            str: The name of the decision.
        """
        return self.name

    class Meta:
        """
        Meta class for Decision model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Decision"
        verbose_name_plural = "Decisions"
