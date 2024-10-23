"""
Module defining the SliderImage model for representing images within slider sections of blog posts.
"""

from django.db import models

from app.cms.models.BlogSection import BlogSection


class SliderImage(models.Model):
    """
    Model representing an image within a slider section of a blog post.

    Attributes:
        image (ImageField): Image file for the slider image, stored in 'SectionSliderImages/'
         directory.
        section (ForeignKey): BlogSection to which the slider image belongs, related_name is
        'slider_images'.


    """

    image = models.ImageField(upload_to="SectionSliderImages/")
    section = models.ForeignKey(
        BlogSection,
        related_name="section_slider_images",
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
