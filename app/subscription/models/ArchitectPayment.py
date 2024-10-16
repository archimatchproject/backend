"""
Module containing the Payment model.

This module defines the Payment model, which includes fields for handling payment information
related to subscription plans, including payment methods, status, and administrative responsibility.

Classes:
    Payment: Define the Payment model with fields and relationships for handling payments.
"""

from django.db import models
from app.subscription.models.ArchitectSelectedSubscriptionPlan import ArchitectSelectedSubscriptionPlan
from app.subscription.models.Payment import Payment
from app.users.models.Architect import Architect


class ArchitectPayment(Payment):
    """
    Define the ArchitectPayment model, which inherits from Payment and adds a relation to an Architect.
    """

    architect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(ArchitectSelectedSubscriptionPlan, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.architect.user.email} - {self.subscription_plan.plan_name}"

