"""
Module containing the SupplierSubscriptionPlan model and its derived models.
"""

from django.db import models
from app.subscription.models.SubscriptionPlan import SubscriptionPlan


class SupplierSubscriptionPlan(SubscriptionPlan):
    """
    Model representing a subscription plan specific to suppliers.
    """

    collection_number = models.PositiveIntegerField()
    product_number_per_collection = models.PositiveIntegerField()

    class Meta:
        """
        Meta class for SupplierSubscriptionPlan model.
        """
        verbose_name = "Supplier Subscription Plan"
        verbose_name_plural = "Supplier Subscription Plans"