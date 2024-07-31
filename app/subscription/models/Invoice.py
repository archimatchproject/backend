"""
Module containing the Invoice model.

This module defines the Invoice model, which includes fields for handling invoice information
related to payments and subscription plans.

Classes:
    Invoice: Defines the Invoice model with fields and relationships for handling invoices.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.users.models.Architect import Architect


class Invoice(BaseModel):
    """
    Define the Invoice model with fields and relationships for handling invoices.

    Fields:
        invoice_number (CharField): A unique identifier for the invoice.
        architect (ForeignKey): The architect making the payment, linked to an Architect instance.
        plan_name (CharField): The name of the subscription plan.
        plan_price (DecimalField): The price of the subscription plan.
        discount (BooleanField): Whether a discount was applied.
        discount_percentage (DecimalField): The percentage of the discount.
        discount_message (CharField): The message associated with the discount.
        amount (DecimalField): The total amount of the invoice.
        date (DateField): The date the invoice was issued.
        due_date (DateField): The date the invoice is due.
        status (CharField): The status of the invoice, either 'Unpaid', 'Paid', or 'Overdue'.
    """

    invoice_number = models.CharField(max_length=50, unique=True)
    architect = models.ForeignKey(Architect, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=255)
    plan_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount_message = models.CharField(max_length=255, default="", null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

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

        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically calculate the amount
        based on the subscription plan price and discount.
        """
        if self.discount and self.discount_percentage:
            self.amount = self.plan_price * (1 - self.discount_percentage / 100)
        else:
            self.amount = self.plan_price
        super().save(*args, **kwargs)
