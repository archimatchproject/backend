"""
Admin configuration for the GuideSection model.

This module defines the admin interface for the GuideSection model,
providing a customizable interface for managing guide sections.
"""

from django.contrib import admin

from app.cms.models.GuideSection import GuideSection


class GuideSectionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing GuideSection instances.
    """

    list_display = ("guide_article", "section_type", "content")
    search_fields = ("guide_article__title", "section_type")
    list_filter = ("section_type",)


admin.site.register(GuideSection, GuideSectionAdmin)
