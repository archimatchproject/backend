from django.db import models


class Blog(models.Model):
    """
    Model representing a blog post.

    Attributes:
        title (CharField): Title of the blog post, maximum length of 255 characters.
        cover_photo (ImageField): Optional cover photo for the blog post, stored in 'BlogsCoverPhotos/' directory.
    """

    title = models.CharField(max_length=255)
    cover_photo = models.ImageField(
        upload_to="BlogsCoverPhotos/", blank=True, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        """Meta class for Blog model."""

        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
