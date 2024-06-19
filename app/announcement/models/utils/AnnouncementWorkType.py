from django.db import models


class AnnouncementWorkType(models.Model):
    """
    Model representing work types for announcements in the Archimatch application.

    Attributes:
        header (CharField): Header or title of the work type, maximum length of 255 characters.
        description (CharField): Description of the work type, maximum length of 255 characters.
    """

    header = models.CharField(max_length=255, default="")
    description = models.CharField(max_length=255, default="")

    def __str__(self) -> str:
        return self.header
