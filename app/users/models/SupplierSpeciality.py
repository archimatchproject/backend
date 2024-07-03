"""
Module: SupplierSpeciality

This module defines the SupplierSpeciality, representing a supplier in the Archimatch application.
"""

from django.db import models


class SupplierSpeciality(models.Model):
    """
    Model representing a SupplierSpeciality in the Archimatch application.


    """

    label = models.CharField(max_length=255, default="")
    icon = models.ImageField(upload_to="SupplierSpecialityIcons/")

    def __str__(self):
        """
        Return a string representation of the labeled icon.

        Returns:
            str: Label or name associated with the icon.
        """
        return self.label

    class Meta:
        """
        Meta class for Supplier Speciality model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Supplier Speciality"
        verbose_name_plural = "Supplier Specialities"
