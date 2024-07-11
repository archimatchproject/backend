"""
Admin configuration for the GuideThematic model.

This module defines the admin interface for the GuideThematic model,
providing a customizable interface for managing guide thematics.
"""

from django.contrib import admin

from app.cms.models.GuideThematic import GuideThematic


class GuideThematicAdmin(admin.ModelAdmin):
    """
    Admin interface for managing GuideThematic instances.
    """

    list_display = ("label", "icon")
    search_fields = ("label",)


admin.site.register(GuideThematic, GuideThematicAdmin)
