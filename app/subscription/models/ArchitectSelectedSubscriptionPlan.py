"""
Module containing the SelectedSubscriptionPlan model and its derived models.
"""
from django.db import models
from app.subscription.models.PlanService import PlanService
from app.subscription.models.SelectedSubscriptionPlan import SelectedSubscriptionPlan


class ArchitectSelectedSubscriptionPlan(SelectedSubscriptionPlan):
    """
    Model representing a selected subscription plan specific to architects.
    """

    number_tokens = models.PositiveIntegerField()
    remaining_tokens = models.PositiveIntegerField()
    services = models.ManyToManyField(PlanService)

    class Meta:
        """
        Meta class for ArchitectSelectedSubscriptionPlan model.
        """
        verbose_name = "Architect Selected Subscription Plan"
        verbose_name_plural = "Architect Selected Subscription Plans"
