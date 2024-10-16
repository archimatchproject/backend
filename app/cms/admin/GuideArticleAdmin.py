"""
Admin configuration for the GuideArticle model.

This module defines the admin interface for the GuideArticle model,
providing a customizable interface for managing guide articles.
It includes an inline configuration for managing related guide sections.
"""

from django.contrib import admin

from app.cms.models.GuideArticle import GuideArticle
from app.cms.models.GuideSection import GuideSection


class GuideSectionInline(admin.TabularInline):
    """
    Inline configuration for managing GuideSection instances within a GuideArticle.
    """

    model = GuideSection
    extra = 1


class GuideArticleAdmin(admin.ModelAdmin):
    """
    Admin interface for managing GuideArticle instances.
    """

    list_display = ("title", "guide_thematic", "date", "rating")
    search_fields = ("title", "description", "guide_thematic__label")
    list_filter = ("guide_thematic", "date", "rating")
    inlines = [GuideSectionInline]


admin.site.register(GuideArticle, GuideArticleAdmin)
