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
from app.users.models.Supplier import Supplier


class SupplierInvoice(Invoice):
    """
    Define the Invoice model with fields and relationships for handling invoices.

    Fields:
        supplier (ForeignKey): The supplier making the payment, linked to an supplier instance.
    """

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    
    def __str__(self):
        """
        String representation of the Invoice instance.

        Returns:
            str: A string representation of the invoice instance, typically
            using the invoice number and status.
        """
        return f"Invoice {self.supplier}"

    class Meta:
        """
        Meta class for Invoice model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """
        
        verbose_name = "SupplierInvoice"
        verbose_name_plural = "SupplierInvoices"

    