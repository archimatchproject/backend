"""
Module containing the Invoice model for offices.

This module defines the OfficeInvoice model, which includes fields for handling invoice information
related to payments and subscription plans for offices.

Classes:
    OfficeInvoice: Defines the Invoice model with fields and relationships for
      handling invoices for offices.
"""

from django.db import models

from app.subscription.models.Invoice import Invoice
from app.users.models.Office import Office


class OfficeInvoice(Invoice):
    """
    Define the Invoice model with fields and relationships for handling
    invoices related to office subscriptions.

    Fields:
        office (ForeignKey): The office making the payment, linked to an office instance.
    """

    office = models.ForeignKey(Office, on_delete=models.CASCADE)

    def __str__(self):
        """
        String representation of the Invoice instance.

        Returns:
            str: A string representation of the invoice instance, typically
            using the invoice number and status.
        """
        return f"Invoice for {self.office}"

    class Meta:
        """
        Meta class for OfficeInvoice model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Office Invoice"
        verbose_name_plural = "Office Invoices"
