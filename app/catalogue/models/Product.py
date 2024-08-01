"""
Module containing the Product model.

This module defines the Product model, which includes fields for handling
product information
related to collections, including name, price, description, and images.
"""

from django.db import models

from app.catalogue.models.Collection import Collection


class Product(models.Model):
    """
    Define the Product model with fields for handling products.

    Fields:
        name (CharField): The name of the product.
        price (DecimalField): The price of the product, optional field.
        collection (ForeignKey): The collection to which the product belongs,
        linked to a Collection instance.
        description (TextField): The description of the product.
        order (PositiveIntegerField): The order of the product in the collection.
        display (BooleanField): Whether the product is displayed or not.
    """

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    display = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the Product instance.

        Returns:
            str: A string representation of the product instance, typically
            using the product name.
        """
        return self.name

    class Meta:
        """
        Meta class for Product model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["order"]
