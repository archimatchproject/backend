from django.db import models


class ArchitectType(models.Model):
    """
    Model representing types of architects.

    Attributes:
        display (CharField): Name or display title of the architect type, maximum length of 255 characters.
        icon (ImageField): Optional icon representing the architect type, stored in 'ArchitectTypeIcons/' directory.
        short_def (TextField): Brief description or definition of the architect type, maximum length of 1000 characters.
    """

    display = models.CharField(max_length=255)
    icon = models.ImageField(blank=True, null=True, upload_to="ArchitectTypeIcons/")
    short_def = models.TextField(max_length=1000)

    def __str__(self):
        return self.display
