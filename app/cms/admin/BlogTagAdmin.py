"""
Admin configuration for the BlogTag model.

This module defines the admin interface for the BlogTag model,
providing a customizable interface for managing guide thematics.
"""

from django.contrib import admin

from app.cms.models.BlogTag import BlogTag


class BlogTagAdmin(admin.ModelAdmin):
    """
    Admin interface for managing BlogTag instances.
    """

    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(BlogTag, BlogTagAdmin)
