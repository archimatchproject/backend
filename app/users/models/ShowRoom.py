"""
Module: ShowRoom Model

This module defines the ShowRoom model, representing a ShowRoom in the Archimatch application.

Classes:
    ShowRoom: Model representing a ShowRoom.
"""
from django.db import models

class ShowRoom(models.Model):
    """
    Model representing a showroom for a supplier.

    Attributes:
        address (CharField): The address of the showroom.
        phone_number (CharField): The phone number of the showroom.
        supplier (ForeignKey): The supplier to whom the showroom belongs.
    """
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    supplier = models.ForeignKey("users.Supplier", related_name="showrooms", on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns the showroom's address.

        Returns:
            str: Address of the showroom.
        """
        return self.address

    class Meta:
        """
        Meta class for Showroom model.

        Attributes:
            verbose_name (str): Singular name for the model used in the Django admin interface.
            verbose_name_plural (str): Plural name for the model used in the Django admin interface.
        """
        verbose_name = "Showroom"
        verbose_name_plural = "Showrooms"
