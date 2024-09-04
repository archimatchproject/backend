"""
Module containing the SubscriptionPlan model and its derived models.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework import serializers
from app.core.models.BaseModel import BaseModel
from app.subscription.models.EventDiscount import EventDiscount
from app.subscription.models.PlanService import PlanService
from datetime import date

class SubscriptionPlan(BaseModel):
    """
    Base model representing a subscription plan.
    """

    plan_name = models.CharField(max_length=255)
    plan_price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    free_plan = models.BooleanField(default=False)
    discount = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    discount_message = models.CharField(max_length=255, default="", null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

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
                or not self.discount_message
            ):
                raise serializers.ValidationError(
                    "the following fields are required: 'discount_percentage', 'start_date', "
                    "'end_date', and 'discount_message'."
                )
        else:
            self.discount_percentage = None
            self.start_date = None
            self.end_date = None
            self.discount_message = None
        
    def get_effective_price(self):
        """
        Returns the effective price of the plan considering any active event discounts.
        """
        price = self.plan_price

        # Apply event discount if applicable
        active_event = EventDiscount.objects.filter(start_date__lte=date.today(), end_date__gte=date.today()).first()
        if active_event:
            price -= (price * active_event.discount_percentage / 100)

        return price

    def __str__(self):
        """
        String representation of the SubscriptionPlan instance.
        """
        return self.plan_name

    class Meta:
        """
        Meta class for SubscriptionPlan model.
        """
        abstract = True
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"