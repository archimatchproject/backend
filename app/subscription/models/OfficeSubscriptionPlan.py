"""
Module containing the OfficeSubscriptionPlan model and its derived models.
"""

from django.db import models

from app.subscription.models.SubscriptionPlan import SubscriptionPlan


class OfficeSubscriptionPlan(SubscriptionPlan):
    """
    Model representing a subscription plan specific to offices.
    """

    announces_number = models.PositiveIntegerField()
    architects_number_per_announce = models.PositiveIntegerField()

    class Meta:
        """
        Meta class for OfficeSubscriptionPlan model.
        """

        verbose_name = "Office Subscription Plan"
        verbose_name_plural = "Office Subscription Plans"
