"""
Django admin configuration for managing CMS sections and slider images.

This module defines admin classes and inlines for managing Section and SliderImage models
in the Django admin interface.
"""

from django.contrib import admin

from app.cms.models import Section
from app.cms.models import SliderImage


class SliderImageInline(admin.TabularInline):
    """
    Inline admin configuration for SliderImage model.

    This inline admin class allows managing SliderImage instances within the SectionAdmin.
    """

    model = SliderImage
    extra = 1


class SectionInline(admin.StackedInline):
    """
    Inline admin configuration for Section model with nested SliderImageInline.

    This inline admin class is used within SectionAdmin to manage Section instances,
    optionally with nested SliderImage instances based on section_type.
    """

    model = Section
    extra = 1
    inlines = [SliderImageInline]

    def get_inline_instances(self, request, obj=None):
        """
        Override to conditionally include SliderImageInline based on obj's section_type.

        Args:
            request (HttpRequest): The current HTTP request.
            obj (Section or None): The Section instance being edited.

        Returns:
            list: List of inline instances to display.
        """
        if obj and obj.section_type == "slider":
            return [SliderImageInline(self.model, self.admin_site)]
        return super().get_inline_instances(request, obj)


class SectionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Section model.

    This admin class provides customizations for the Section model in the Django
     admin site.
    It includes list display fields, filters, and inline editing for associated
     SliderImage instances.
    """

    list_display = (
        "section_type",
        "blog",
        "content",
    )
    list_filter = ("section_type", "blog")

    inlines = [SliderImageInline]

    def get_inline_instances(self, request, obj=None):
        """
        Override to conditionally include SliderImageInline based on obj's section_type.

        Args:
            request (HttpRequest): The current HTTP request.
            obj (Section or None): The Section instance being edited.

        Returns:
            list: List of inline instances to display.
        """
        if obj and obj.section_type == "slider":
            return [SliderImageInline(self.model, self.admin_site)]
        return super().get_inline_instances(request, obj)


admin.site.register(Section, SectionAdmin)