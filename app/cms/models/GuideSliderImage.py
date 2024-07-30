"""
Module defining the GuideSliderImage model for representing images within
slider sections of guide posts.
"""

from django.db import models

from app.cms.models.GuideSection import GuideSection


class GuideSliderImage(models.Model):
    """
    Model representing an image within a slider section of a guide post.

    Attributes:
        image (ImageField): Image file for the slider image, stored in 'SectionGuideSliderImages/'
         directory.
        section (ForeignKey): GuideSection to which the slider image belongs, related_name is
        'slider_images'.


    """

    image = models.ImageField(upload_to="SectionGuideSliderImages/")
    section = models.ForeignKey(
        GuideSection,
        related_name="section_slider_images",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        """
        String representation of the GuideSliderImage instance.
        Returns:
            str: URL of the image.
        """
        return self.image.url

    class Meta:
        """
        Meta class for Slider Image model.

        Defines display names for singular and plural forms of Slider
        Image in the Django admin.
        """

        verbose_name = "Slider Image"
        verbose_name_plural = "Slider Images"
