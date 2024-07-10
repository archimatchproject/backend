"""
Module defining the Section model for representing sections within a blog post.
"""

from django.db import models

from app.cms.models.Blog import Blog


class Section(models.Model):
    """
    Model representing a section within a blog post.

    Attributes:
        BLOG_SECTION_TYPES (list): Choices for types of sections within a blog post.
        blog (ForeignKey): Blog to which the section belongs, related_name is 'sections'.
        section_type (CharField): Type of the section, selected from BLOG_SECTION_TYPES.
        content (TextField): Optional content of the section.
        image (ImageField): Optional image associated with the section, stored in 'SectionImages/'
          directory.
    """

    BLOG_SECTION_TYPES = [
        ("title", "Title"),
        ("paragraph", "Paragraph"),
        ("image", "Image"),
        ("slider", "Slider"),
    ]

    blog = models.ForeignKey(
        Blog,
        related_name="blog_sections",
        on_delete=models.CASCADE,
    )
    section_type = models.CharField(
        max_length=10,
        choices=BLOG_SECTION_TYPES,
        default=BLOG_SECTION_TYPES[0],
    )
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="SectionImages/",
        blank=True,
        null=True,
    )

    def __str__(self):
        """
        String representation of the section.
        """
        return f"{self.get_section_type_display()} for {self.blog.title}"

    class Meta:
        """
        Meta class for Section model.

        Defines display names for singular and plural forms of Section in the Django admin.
        """

        verbose_name = "Section"
        verbose_name_plural = "Sections"
