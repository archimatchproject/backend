"""
Module: Supplier Model

This module defines the Supplier model, representing a supplier in the Archimatch application.

Classes:
    Supplier: Model representing a supplier.
"""

from django.db import models

from app.core.models import BaseModel
from app.core.models.SupplierSpeciality import SupplierSpeciality
from app.users.models import ArchimatchUser
from app.users.models.SupplierSocialMedia import SupplierSocialMedia


class Supplier(BaseModel):
    """
    Model representing a supplier in the Archimatch application.

    Attributes:
        profile_image (ImageField): Profile image of the supplier, stored in
        'SupplierProfileImages/' directory.
        cover_image (ImageField): Cover image of the supplier, stored in
        'SupplierCoverImages/' directory.
        is_public (BooleanField): Indicates if the supplier's profile is public.
        company_address (CharField): Address of the supplier's company, maximum length
        of 255 characters.
        company_speciality (CharField): Specialization or field of expertise of the supplier's
        company, maximum length of 255 characters.
        bio (TextField): Biography or description of the supplier, maximum length of 500 characters.
        company_name (CharField): Name of the company associated with the supplier,
        maximum length of 255 characters.
        presentation_video (FileField): Video presentation file uploaded by the supplier,
        stored in 'SupplierVideos/' directory.
        speciality_type (ManyToManyField): Many-to-many relationship with SupplierSpeciality
        for the supplier's specialities.
        social_links (OneToOneField): Associated SupplierSocialMedia instance for social media
        links, optional.
        user (OneToOneField): Associated ArchimatchUser instance for this supplier.
    """

    profile_image = models.ImageField(
        blank=True,
        null=True,
        upload_to="SupplierProfileImages/",
    )
    cover_image = models.ImageField(
        blank=True,
        null=True,
        upload_to="SupplierCoverImages/",
    )
    is_public = models.BooleanField(default=False)
    company_address = models.CharField(max_length=255, default="")
    company_speciality = models.CharField(max_length=255, default="")
    bio = models.TextField(max_length=500, default="")
    company_name = models.CharField(max_length=255, default="")
    presentation_video = models.FileField(
        upload_to="SupplierVideos/",
        blank=True,
        null=True,
    )
    speciality_type = models.ManyToManyField(
        SupplierSpeciality,
        related_name="speciality_type_suppliers",
    )
    social_links = models.OneToOneField(
        SupplierSocialMedia,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)
    catalog_visibility = models.BooleanField(default=False)
    subscription_plan = models.ForeignKey(
        "subscription.SupplierSelectedSubscriptionPlan",
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True,
    )
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
