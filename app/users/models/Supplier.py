from django.db import models

from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.models.utils.SocialMedia import SocialMedia
from app.utils.models import BaseModel


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

    address = models.CharField(max_length=255, default="")
    speciality = models.CharField(max_length=255, default="")
    bio = models.TextField(max_length=1000, default="")
    company_name = models.CharField(max_length=255, default="")
    presentation_video = models.FileField(
        upload_to="SupplierVideos/", blank=True, null=True
    )
    type = models.TextField(max_length=1000, default="")
    social_links = models.OneToOneField(
        SocialMedia, blank=True, null=True, on_delete=models.CASCADE
    )
    user = models.OneToOneField(ArchimatchUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
