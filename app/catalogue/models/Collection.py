"""
Module containing the Collection model.

This module defines the Collection model, which includes fields for handling
collection information
related to suppliers, including the title and category.
"""

from django.db import models

from app.catalogue import APPEARANCES
from app.core.models.SupplierSpeciality import SupplierSpeciality
from app.users.models.Supplier import Supplier


class Collection(models.Model):
    """
    Define the Collection model with fields for handling collections.

    Fields:
        title (CharField): The title of the collection.
        category (ForeignKey): The category of the collection, linked to a
        SupplierSpeciality instance.
        appearance (CharField): Appearance attribute of the collection, choices defined by
        APPEARANCES, maximum length of 10 characters.
    """

    title = models.CharField(max_length=255)
    category = models.ForeignKey(SupplierSpeciality, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="supplier_collections"
    )
    appearance = models.CharField(
        max_length=10,
        choices=APPEARANCES,
        default="Petite",
    )
    display = models.BooleanField(default=False)
    visibility = models.BooleanField(default=False)
    def __str__(self):
        """
        String representation of the Collection instance.

        Returns:
            str: A string representation of the collection instance, typically
            using the collection title.
        """
        return self.title

    class Meta:
        """
        Meta class for Collection model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Collection"
        verbose_name_plural = "Collections"
