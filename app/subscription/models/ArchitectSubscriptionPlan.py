"""
Module containing the ArchitectSubscriptionPlan model and its derived models.
"""

from django.db import models
from app.core.models.BaseModel import BaseModel
from app.subscription.models.PlanService import PlanService
from app.subscription.models.SubscriptionPlan import SubscriptionPlan


class ArchitectSubscriptionPlan(SubscriptionPlan):
    """
    Model representing a subscription plan specific to architects.
    """
    number_tokens = models.PositiveIntegerField()
    number_free_tokens = models.PositiveIntegerField()
    services = models.ManyToManyField(PlanService)

    class Meta:
        """
        Meta class for ArchitectSubscriptionPlan model.
        """
        verbose_name = "Architect Subscription Plan"
        verbose_name_plural = "Architect Subscription Plans"