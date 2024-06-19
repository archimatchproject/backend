from django.db import models

from app.cms.models.Block import Block


class SliderImage(models.Model):
    """
    Model representing an image within a slider block of a blog post.

    Attributes:
        image (ImageField): Image file for the slider image, stored in 'BlockSliderImages/' directory.
        block (ForeignKey): Block to which the slider image belongs, related_name is 'slider_images'.

    Methods:
        __str__(): Returns the URL of the image.
    """

    image = models.ImageField(upload_to="BlockSliderImages/")
    block = models.ForeignKey(
        Block, related_name="slider_images", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.image.url

    class Meta:
        """Meta class for Slider Image model."""

        verbose_name = "Slider Image"
        verbose_name_plural = "Slider Images"
