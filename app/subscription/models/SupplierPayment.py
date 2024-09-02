"""
Module containing the Payment model.

This module defines the Payment model, which includes fields for handling payment information
related to subscription plans, including payment methods, status, and administrative responsibility.

Classes:
    Payment: Define the Payment model with fields and relationships for handling payments.
"""
from django.db import models
from app.subscription.models.Payment import Payment
from app.users.models.Supplier import Supplier


class SupplierPayment(Payment):
    """
    Define the SupplierPayment model, which inherits from Payment and adds a relation to a Supplier.
    """

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.supplier.user.email} - {self.subscription_plan.plan_name}"
