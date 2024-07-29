"""
Module: SupplierSpeciality

This module defines the SupplierSpeciality, representing a supplier in the Archimatch application.
"""

from django.db import models

from app.core.models import LabeledIcon


class SupplierSpeciality(LabeledIcon):
    """
    Model representing a SupplierSpeciality in the Archimatch application.


    """

    icon = models.ImageField(upload_to="icons/SupplierSpecialityIcons/")

    class Meta:
        """
        Meta class for Supplier Speciality model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Supplier Speciality"
        verbose_name_plural = "Supplier Specialities"
