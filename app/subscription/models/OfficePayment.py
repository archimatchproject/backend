"""
Module containing the Payment model for offices.

This module defines the OfficePayment model, which includes fields for handling payment information
related to subscription plans for offices, including payment methods, status,
 and administrative responsibility.

Classes:
    OfficePayment: Defines the Payment model with fields and
    relationships for handling office payments.
"""

from django.db import models

from app.subscription.models.OfficeSelectedSubscriptionPlan import OfficeSelectedSubscriptionPlan
from app.subscription.models.Payment import Payment
from app.users.models.Office import Office


class OfficePayment(Payment):
    """
    Define the OfficePayment model, which inherits from Payment and adds a relation to an Office.
    """

    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(OfficeSelectedSubscriptionPlan, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the OfficePayment instance.
        The string includes the office name and the subscription plan name.
        Returns:
            str: A string in the format "office_name - plan_name".
        """

        return f"{self.office.office_name} - {self.subscription_plan.plan_name}"
