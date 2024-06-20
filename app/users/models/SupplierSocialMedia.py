"""
Module: Supplier Social Media Model

This module defines the SupplierSocialMedia model, representing social media links for suppliers in the Archimatch application.

Classes:
    SupplierSocialMedia: Model representing social media links for suppliers.

"""

from django.db import models

from app.utils.models import BaseModel


class SupplierSocialMedia(BaseModel):
    """
    Model representing social media links for suppliers in the Archimatch application.

    Attributes:
        facebook (CharField): Facebook profile link of the supplier, maximum length of 255 characters.
        instagram (CharField): Instagram profile link of the supplier, maximum length of 255 characters.
        website (CharField): Website link of the supplier, maximum length of 255 characters.
    """

    facebook = models.CharField(max_length=255, default="")
    instagram = models.CharField(max_length=255, default="")
    website = models.CharField(max_length=255, default="")

    def __str__(self):
        """
        Returns the Facebook profile link of the supplier.

        Returns:
            str: Facebook profile link of the supplier.
        """
        return self.facebook

    class Meta:
        """
        Meta class for Supplier Social Media model.

        Attributes:
            verbose_name (str): Singular name for the model used in the Django admin interface.
            verbose_name_plural (str): Plural name for the model used in the Django admin interface.
        """

        verbose_name = "Supplier Social Media"
        verbose_name_plural = "Supplier Social Medias"
