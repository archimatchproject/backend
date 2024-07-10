"""
Module defining the GuideSection model for representing sections within a guide article.
"""

from django.db import models


# from app.cms.models.GuideArticle import GuideArticle


class GuideSection(models.Model):
    """
    Model representing a section within a guide article.

    Attributes:
        GUIDE_SECTION_TYPES (list): Choices for types of sections within a guide article.
        guide_article (ForeignKey): Guide article to which the section belongs.
        section_type (CharField): Type of the section, selected from GUIDE_SECTION_TYPES.
        content (TextField): Optional content of the section.
        image (ImageField): Optional image associated with the section,
        stored in 'GuideSectionImages/' directory.
        video (FileField): Optional video associated with the section,
        stored in 'GuideSectionVideos/' directory.
    """

    GUIDE_SECTION_TYPES = [
        ("title", "Title"),
        ("paragraph", "Paragraph"),
        ("image", "Image"),
        ("video", "Video"),
    ]

    # guide_article = models.ForeignKey(
    #     GuideArticle,
    #     related_name="guide_article_sections",
    #     on_delete=models.CASCADE,
    # )
    section_type = models.CharField(
        max_length=10,
        choices=GUIDE_SECTION_TYPES,
        default="title",
    )
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="GuideSectionImages/", blank=True, null=True)
    video = models.FileField(upload_to="GuideSectionVideos/", blank=True, null=True)

    def __str__(self):
        """
        String representation of the section.
        """
        return f"{self.get_section_type_display()} for {self.guide_article.title}"

    class Meta:
        """
        Meta class for GuideSection model.

        Defines display names for singular and plural forms of GuideSection in the Django admin.
        """

        verbose_name = "GuideSection"
        verbose_name_plural = "GuideSections"
