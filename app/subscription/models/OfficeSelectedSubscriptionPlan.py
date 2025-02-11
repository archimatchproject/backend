"""
Module containing the SelectedSubscriptionPlan model and its derived models.
"""

from django.db import models
from app.subscription.models.SelectedSubscriptionPlan import SelectedSubscriptionPlan


class OfficeSelectedSubscriptionPlan(SelectedSubscriptionPlan):
    """
    Model representing a selected subscription plan specific to offices.
    """

    announces_number = models.PositiveIntegerField()
    architects_number_per_announce = models.PositiveIntegerField()

    class Meta:
        """
        Meta class for OfficeSelectedSubscriptionPlan model.
        """
        verbose_name = "Office Selected Subscription Plan"
        verbose_name_plural = "Office Selected Subscription Plans"
