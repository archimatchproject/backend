"""
Module: Supplier Model

This module defines the Supplier model, representing a supplier in the Archimatch application.

Classes:
    Supplier: Model representing a supplier.
"""

from django.db import models

from app.core.models import BaseModel
from app.users import APPEARANCES
from app.users.models import ArchimatchUser
from app.users.models.SupplierSocialMedia import SupplierSocialMedia
from app.users.models.SupplierSpeciality import SupplierSpeciality


class Supplier(BaseModel):
    """
    Model representing a supplier in the Archimatch application.

    Attributes:
        address (CharField): Address of the supplier, maximum length of 255 characters.
        speciality (CharField): Specialization or field of expertise of the supplier, maximum length of 255 characters.
        bio (TextField): Biography or description of the supplier, maximum length of 1000 characters.
        company_name (CharField): Name of the company associated with the supplier, maximum length of 255 characters.
        presentation_video (FileField): Video presentation file uploaded by the supplier, stored in 'SupplierVideos/' directory.
        type (TextField): Type or category of the supplier, maximum length of 1000 characters.
        social_links (OneToOneField): Associated SocialMedia instance for social media links, optional.
        user (OneToOneField): Associated ArchimatchUser instance for this supplier.
    """

    company_address = models.CharField(max_length=255, default="")
    company_speciality = models.CharField(max_length=255, default="")
    bio = models.TextField(max_length=1000, default="")
    company_name = models.CharField(max_length=255, default="")
    presentation_video = models.FileField(upload_to="SupplierVideos/", blank=True, null=True)
    speciality_type = models.ManyToManyField(
        SupplierSpeciality, related_name="speciality_type_suppliers"
    )
    appearance = models.CharField(max_length=10, choices=APPEARANCES, default="Petite")
    social_links = models.OneToOneField(
        SupplierSocialMedia, blank=True, null=True, on_delete=models.CASCADE
    )
    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns the email address of the associated user.

        Returns:
            str: Email address of the supplier's associated user.
        """
        return self.user.email

    class Meta:
        """
        Meta class for Supplier model.

        Attributes:
            verbose_name (str): Singular name for the model used in the Django admin interface.
            verbose_name_plural (str): Plural name for the model used in the Django admin interface.
        """

        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
