"""
Django admin configuration for managing Blog instances.

This module defines admin classes and configurations for managing Blog instances
and related SectionInline instances in the Django admin interface.
"""

from django.contrib import admin

from app.cms.admin.BlogSectionAdmin import SectionInline
from app.cms.models.Blog import Blog


class BlogAdmin(admin.ModelAdmin):
    """
    Admin configuration for Blog model.

    This admin class provides customizations for the Blog model in the Django admin site.
    It includes inlines for managing associated BlogSection instances and specifies
    list display fields.
    """

    model = Blog
    inlines = [SectionInline]
    list_display = ("title",)


admin.site.register(Blog, BlogAdmin)
