"""
Admin configuration for the BlogThematic model.

This module defines the admin interface for the BlogThematic model,
providing a customizable interface for managing guide thematics.
"""

from django.contrib import admin

from app.cms.models.BlogThematic import BlogThematic


class BlogThematicAdmin(admin.ModelAdmin):
    """
    Admin interface for managing BlogThematic instances.
    """

    list_display = ("title",)
    search_fields = ("title",)


admin.site.register(BlogThematic, BlogThematicAdmin)
