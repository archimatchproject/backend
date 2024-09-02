"""
Module containing the Payment model.

This module defines the Payment model, which includes fields for handling payment information
related to subscription plans, including payment methods, status, and administrative responsibility.

Classes:
    Payment: Define the Payment model with fields and relationships for handling payments.
"""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from app.core.models.BaseModel import BaseModel
from app.core.models.Note import Note
from app.subscription import PAYMENT_METHOD_CHOICES
from app.subscription import PAYMENT_STATUS_CHOICES
from app.subscription.models.Payment import Payment
from app.subscription.models.SelectedSubscriptionPlan import SelectedSubscriptionPlan
from app.users.models.Admin import Admin
from app.users.models.Architect import Architect


class ArchitectPayment(Payment):
    """
    Define the ArchitectPayment model, which inherits from Payment and adds a relation to an Architect.
    """

    architect = models.ForeignKey(Architect, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.architect.user.email} - {self.subscription_plan.plan_name}"

