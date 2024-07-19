"""
Module defining the Blog model.

This module contains the Blog class, which represents a blog post in the application.
"""

from django.db import models

from app.cms.models.BlogTag import BlogTag
from app.cms.models.BlogThematic import BlogThematic
from app.core.models.BaseModel import BaseModel
from app.users.models.Admin import Admin


class Blog(BaseModel):
    """
    Model representing a blog post.

    Attributes:
        title (str): The title of the blog post.
        sub_title (str): The subtitle of the blog post.
        content (TextField): The content of the blog post.
        blog_thematic (ForeignKey): The thematic category to which the blog post belongs.
        tags (ManyToManyField): Tags associated with the blog post.
        admin (ForeignKey): The admin who created the blog post.
        visible (bool): Whether the blog post is visible.
        last_update (DateTimeField): The date and time of the last update.
    """

    title = models.CharField(max_length=255)
    cover_photo = models.ImageField(
        upload_to="BlogsCoverPhotos/",
        blank=True,
        null=True,
    )
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    blog_thematic = models.ForeignKey(
        BlogThematic, on_delete=models.CASCADE, related_name="blog_thematic_blogs"
    )
    tags = models.ManyToManyField(BlogTag)
    admin = models.ForeignKey(Admin, on_delete=models.DO_NOTHING)
    visible = models.BooleanField(default=False)

    class Meta:
        """
        Meta class for Blog model.

        Provides verbose names for the model in the Django admin interface.
        """

        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        """
        String representation of the blog.
        """
        return self.title
