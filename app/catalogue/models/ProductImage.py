"""
Module containing the ProductImage model.

This module defines the ProductImage model, which includes fields for handling product images.
"""

from django.db import models

from app.catalogue.models.Product import Product


class ProductImage(models.Model):
    """
    Define the ProductImage model with fields for handling product images.

    Fields:
        product (ForeignKey): The product to which the image belongs, linked to a Product instance.
        image (ImageField): The image associated with the product.
    """

    product = models.ForeignKey(Product, related_name="product_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        """
        String representation of the ProductImage instance.

        Returns:
            str: A string representation of the product image instance, typically
            using the product name and image id.
        """
        return f"{self.product.name} Image {self.product.name}"

    class Meta:
        """
        Meta class for ProductImage model.

        Meta Attributes:
            verbose_name (str): The name of the model in singular form.
            verbose_name_plural (str): The name of the model in plural form.
        """

        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
