"""
Module containing the SelectedSubscriptionPlan model and its derived models.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework import serializers
from app.core.models.BaseModel import BaseModel
from app.subscription.models.PlanService import PlanService


class SelectedSubscriptionPlan(BaseModel):
    """
    Base model representing a selected subscription plan.
    """

    plan_name = models.CharField(max_length=255)
    plan_price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    free_plan = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    discount = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def save(self, *args, **kwargs):
        """
        Custom save method to ensure the plan price is zero if the plan is free.
        """
        if self.free_plan:
            self.plan_price = 0
        super().save(*args, **kwargs)

    def clean(self):
        """
        Custom validation method to ensure valid discount fields.
        """
        if self.discount:
            if (
                self.discount_percentage is None
                or self.start_date is None
                or self.end_date is None
            ):
                raise serializers.ValidationError(
                    "The following fields are required: 'discount_percentage', 'start_date', and 'end_date'."
                )
        else:
            self.discount_percentage = None
            self.start_date = None
            self.end_date = None

    def __str__(self):
        """
        String representation of the SelectedSubscriptionPlan instance.
        """
        return self.plan_name

    class Meta:
        """
        Meta class for SelectedSubscriptionPlan model.
        """
        abstract = True
        verbose_name = "Selected Subscription Plan"
        verbose_name_plural = "Selected Subscription Plans"
