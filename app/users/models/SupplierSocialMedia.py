from django.db import models

from app.utils.models import BaseModel


class SupplierSocialMedia(BaseModel):

    facebook = models.CharField(max_length=255, default="")
    instagram = models.CharField(max_length=255, default="")
    website = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.facebook

    class Meta:
        """Meta class for Supplier Social Media model."""

        verbose_name = "Supplier Social Media"
        verbose_name_plural = "Supplier Social Medias"
