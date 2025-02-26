"""
QuoteService model module for defining quote-related services.

This file contains the QuoteService model, which represents a specific service or
product with details such as title, description, unit, category, and unit price.
This model is designed to store and manage the services or products included in quotes.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel
from app.quote.models.Category import Category
from app.quote.models.Unit import Unit


class QuoteService(BaseModel):
    """
    Model to represent a quote service.

    A QuoteService is a combination of title, description, unit, category, and unit price,
    representing a specific service or product in a particular category.
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        """
        Meta options for QuoteService model.

        The verbose_name and verbose_name_plural options control how this model
        is displayed in the Django admin interface.
        The unit and category are foreign keys, linking to the Unit and Category models.
        """

        verbose_name = "Quote Service"
        verbose_name_plural = "Quote Services"

    def __str__(self):
        """
        Returns a string representation of the QuoteService instance.
        Returns:
            str: The title of the quote.
        """

        return self.title
