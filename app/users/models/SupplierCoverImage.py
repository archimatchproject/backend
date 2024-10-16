"""
Module defining the SupplierCoverImage model for representing images of a supplier cover.
"""

from django.db import models

from app.users.models.Supplier import Supplier


class SupplierCoverImage(models.Model):
    """
    Model representing an image within a cover of supplier.

    Attributes:
        image (ImageField): Image file for the cover image, stored in 'SupplierCoverImages/'
        directory.
        supplier (ForeignKey): Supplier to which the cover image belongs, related_name is
        'supplier_cover_images'.


    """

    image = models.ImageField(upload_to="SupplierCoverImages/")
    supplier = models.ForeignKey(
        Supplier,
        related_name="supplier_cover_images",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        """
        String representation of the SupplierCoverImage instance.
        Returns:
            str: URL of the image.
        """
        return self.image.url

    class Meta:
        """
        Meta class for SupplierCoverImage model.

        Defines display names for singular and plural forms of SupplierCoverImage in the
        Django admin.
        """

        verbose_name = "Supplier Cover Image"
        verbose_name_plural = "Supplier Cover Images"
