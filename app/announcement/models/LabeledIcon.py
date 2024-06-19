from django.db import models


class LabeledIcon(models.Model):
    """
    Model representing a labeled icon with a label and an associated image.

    Attributes:
        label (CharField): Label or name associated with the icon, maximum length of 255 characters.
        icon (ImageField): Image file representing the icon, stored in 'Icons/' directory.
    """

    label = models.CharField(max_length=255, default="")
    icon = models.ImageField(upload_to="Icons/")

    def __str__(self):
        return self.label

    class Meta:
        """Meta class for Labeled Icon model."""

        verbose_name = "Labeled Icon"
        verbose_name_plural = "Labeled Icons"
