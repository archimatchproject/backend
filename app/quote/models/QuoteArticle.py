"""
QuoteArticle model module for defining quote-related articles.

This file contains the QuoteArticle model, which represents a specific article or
product with details such as title, description, unit, category, and unit price.
This model is designed to store and manage the articles or products included in quotes.
"""

from django.db import models

from app.core.models.BaseModel import BaseModel


class QuoteArticle(BaseModel):
    """
    Model to represent a quote article.

    A QuoteArticle is a combination of title, description, unit, category, and unit price,
    representing a specific article or product in a particular category.
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    byDefault = models.BooleanField(default=False)
    architect = models.ForeignKey("users.Architect", on_delete=models.CASCADE, related_name="quoteArticles")

    class Meta:
        """
        Meta options for QuoteArticle model.

        The verbose_name and verbose_name_plural options control how this model
        is displayed in the Django admin interface.
        The unit and category are foreign keys, linking to the Unit and Category models.
        """

        verbose_name = "Quote article"
        verbose_name_plural = "Quote articles"

    def __str__(self):
        """
        Returns a string representation of the QuoteArticle instance.
        Returns:
            str: The title of the quote.
        """

        return self.title
