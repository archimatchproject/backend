from django.core.exceptions import ValidationError
from django.db import models


class ProjectImage(models.Model):
    """
    Model representing an image associated with a project.

    Attributes:
        image (ImageField): Image file uploaded for the project, stored in 'images/' directory.

    Methods:
        clean(): Custom validation method to ensure no more than 5 images are associated with a project.
        __str__(): Returns a string representation of the image.
    """

    image = models.ImageField(upload_to="images/")

    def clean(self):
        """
        Custom validation to ensure a project's gallery does not exceed 5 images.
        """
        if self.project.images.count() >= 5:
            raise ValidationError("A gallery can contain a maximum of 5 images.")

    def __str__(self):
        return f"Image {self.id} for {self.project.client}"

    class Meta:
        """Meta class for Project Image model."""

        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
