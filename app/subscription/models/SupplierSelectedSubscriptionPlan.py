"""
Module containing the SelectedSubscriptionPlan model and its derived models.
"""
from django.db import models
from app.subscription.models.SelectedSubscriptionPlan import SelectedSubscriptionPlan


class SupplierSelectedSubscriptionPlan(SelectedSubscriptionPlan):
    """
    Model representing a selected subscription plan specific to suppliers.
    """

    collection_number = models.PositiveIntegerField()
    product_number_per_collection = models.PositiveIntegerField()

    class Meta:
        """
        Meta class for SupplierSelectedSubscriptionPlan model.
        """
        verbose_name = "Supplier Selected Subscription Plan"
        verbose_name_plural = "Supplier Selected Subscription Plans"
