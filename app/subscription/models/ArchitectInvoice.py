"""
Module containing the Invoice model.

This module defines the Invoice model, which includes fields for handling invoice information
related to payments and subscription plans.

Classes:
    Invoice: Defines the Invoice model with fields and relationships for handling invoices.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.subscription.models.Invoice import Invoice
from app.users.models.Architect import Architect


class ArchitectInvoice(Invoice):
    """
    Define the Invoice model with fields and relationships for handling invoices.

    Fields:
        architect (ForeignKey): The architect making the payment, linked to an Architect instance.
    """

    architect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    
    def __str__(self):
        """
        String representation of the Invoice instance.

        Returns:
            str: A string representation of the invoice instance, typically
            using the invoice number and status.
        """
        return f"Invoice {self.architect}"

    class Meta:
        """
        Meta class for Invoice model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """
        
        verbose_name = "ArchitectInvoice"
        verbose_name_plural = "ArchitectInvoices"

    