"""
Module containing the SelectedSubscriptionPlan model.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.subscription.models.PlanService import PlanService


class SelectedSubscriptionPlan(BaseModel):
    """
    Model representing a selected subscription plan.
    """

    plan_name = models.CharField(max_length=255)
    plan_price = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_tokens = models.PositiveIntegerField()

    active = models.BooleanField(default=True)
    free_plan = models.BooleanField(default=False)
    services = models.ManyToManyField(PlanService)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Custom save method to ensure the plan price is zero if the plan is free.
        """
        if self.free_plan:
            self.plan_price = 0
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the SelectedSubscriptionPlan instance.
        """
        return self.plan_name

    class Meta:
        """
        Meta class for SelectedSubscriptionPlan model.
        """

        verbose_name = "Selected Subscription Plan"
        verbose_name_plural = "Selected Subscription Plans"
