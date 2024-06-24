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
