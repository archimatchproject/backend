"""
Module: Office Model

This module defines the Office model, representing an Office in the Archimatch application.

Classes:
    Office: Model representing an office.
"""

from django.db import models

from app.core.models import BaseModel
from app.users.models import ArchimatchUser
from app.users.models.SupplierSocialMedia import SupplierSocialMedia


class Office(BaseModel):
    """
    Model representing an office in the Archimatch application.

    Attributes:
        profile_image (ImageField): Profile image of the office, stored in
        'OfficeProfileImages/' directory.
        is_public (BooleanField): Indicates if the office's profile is public.
        office_address (CharField): Address of the office's company, maximum length
        of 255 characters.
        bio (TextField): Biography or description of the office, maximum length of 500 characters.
        office_name (CharField): Name of the office,
        maximum length of 255 characters.
        social_links (OneToOneField): Associated SupplierSocialMedia instance for social media
        links, optional.
        user (OneToOneField): Associated ArchimatchUser instance for this supplier.
    """

    profile_image = models.ImageField(
        blank=True,
        null=True,
        upload_to="OfficeProfileImages/",
    )
    is_public = models.BooleanField(default=False)
    office_address = models.CharField(max_length=255, default="")
    office_identifier = models.CharField(
        max_length=10, default="", null=True, blank=True, unique=True
    )
    bio = models.TextField(max_length=500, default="")
    office_name = models.CharField(max_length=255, default="")
    social_links = models.OneToOneField(
        SupplierSocialMedia,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)

    subscription_plan = models.ForeignKey(
        "subscription.OfficeSelectedSubscriptionPlan",
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        """
        Returns the email address of the associated user.

        Returns:
            str: Email address of the office's associated user.
        """
        return self.user.email

    class Meta:
        """
        Meta class for Office model.

        Attributes:
            verbose_name (str): Singular name for the model used in the Django admin interface.
            verbose_name_plural (str): Plural name for the model used in the Django admin interface.
        """

        verbose_name = "Office"
        verbose_name_plural = "Offices"
