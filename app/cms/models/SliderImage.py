"""
Module defining the SliderImage model for representing images within slider blocks of blog posts.
"""

from django.db import models

from app.cms.models.Block import Block


class SliderImage(models.Model):
    """
    Model representing an image within a slider block of a blog post.

    Attributes:
        image (ImageField): Image file for the slider image, stored in 'BlockSliderImages/'
         directory.
        block (ForeignKey): Block to which the slider image belongs, related_name is
        'slider_images'.


    """

    image = models.ImageField(upload_to="BlockSliderImages/")
    block = models.ForeignKey(
        Block,
        related_name="block_slider_images",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        """
        String representation of the SliderImage instance.
        Returns:
            str: URL of the image.
        """
        return self.image.url

    class Meta:
        """
        Meta class for Slider Image model.

        Defines display names for singular and plural forms of Slider Image in the Django admin.
        """

        verbose_name = "Slider Image"
        verbose_name_plural = "Slider Images"
