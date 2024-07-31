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

    Fields:
        architect (ForeignKey): The architect making the payment, linked to an Architect instance.
        admin_responsable (ForeignKey): The admin responsible for the payment,
        linked to an Admin instance.
        payment_method (CharField): The method of payment chosen from a predefined list.
        status (CharField): The status of the payment, either 'Unpaid' or 'Paid'.
        subscription_plan (ForeignKey): The subscription plan associated with the payment.
        notes (GenericRelation): Generic relation to the Note model for adding
        notes related to the payment.
    """

    architect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    admin_responsable = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default=PAYMENT_METHOD_CHOICES[0][0]
    )
    status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_CHOICES[0][0]
    )
    subscription_plan = models.ForeignKey(SelectedSubscriptionPlan, on_delete=models.CASCADE)
    notes = GenericRelation(Note)

    def __str__(self):
        """
        String representation of the Payment instance.

        Returns:
            str: A string representation of the payment instance, typically
            using the user's email and plan name.
        """
        return f"{self.architect.user.email} - {self.subscription_plan.plan_name}"

    class Meta:
        """
        Meta class for Payment model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Payment"
        verbose_name_plural = "Payments"
