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
from app.subscription.models.SelectedSubscriptionPlan import SelectedSubscriptionPlan
from app.users.models.Admin import Admin
from app.users.models.Architect import Architect


class Payment(BaseModel):
    """
    Define the Payment model with fields and relationships for handling payments.
    """

    admin_responsable = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default=PAYMENT_METHOD_CHOICES[0][0]
    )
    status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_CHOICES[0][0]
    )
    
    notes = GenericRelation(Note)

    def __str__(self):
        return f"{self.status}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
