"""
Module containing the SubscriptionPlan model.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.subscription.models.PlanService import PlanService


class SubscriptionPlan(BaseModel):
    """
    Model representing a subscription plan.
    """

    plan_name = models.CharField(max_length=255)
    plan_price = models.DecimalField(max_digits=10, decimal_places=2)
    number_tokens = models.PositiveIntegerField()
    number_free_tokens = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    free_plan = models.BooleanField(default=False)
    services = models.ManyToManyField(PlanService)

    def save(self, *args, **kwargs):
        """
        Custom save method to ensure the plan price is zero if the plan is free.
        """
        if self.free_plan:
            self.plan_price = 0
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the SubscriptionPlan instance.
        """
        return self.plan_name

    class Meta:
        """
        Meta class for SubscriptionPlan model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"