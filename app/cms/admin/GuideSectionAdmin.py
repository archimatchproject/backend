"""
Admin configuration for the GuideSection model.

This module defines the admin interface for the GuideSection model,
providing a customizable interface for managing guide sections.
"""

from django.contrib import admin

from app.cms.models.GuideSection import GuideSection
from app.cms.models.GuideSliderImage import GuideSliderImage


class GuideSliderImageInline(admin.TabularInline):
    """
    Inline admin configuration for SliderImage model.

    This inline admin class allows managing SliderImage instances within the SectionAdmin.
    """

    model = GuideSliderImage
    extra = 1
    
class GuideSectionInline(admin.StackedInline):
    """
    Inline admin configuration for BlogSection model with nested SliderImageInline.

    This inline admin class is used within SectionAdmin to manage BlogSection instances,
    optionally with nested SliderImage instances based on section_type.
    """

    model = GuideSection
    extra = 1
    inlines = [GuideSliderImageInline]

    def get_inline_instances(self, request, obj=None):
        """
        Override to conditionally include SliderImageInline based on obj's section_type.

        Args:
            request (HttpRequest): The current HTTP request.
            obj (BlogSection or None): The BlogSection instance being edited.

        Returns:
            list: List of inline instances to display.
        """
        if obj and obj.section_type == "slider":
            return [GuideSliderImageInline(self.model, self.admin_site)]
        return super().get_inline_instances(request, obj)

class GuideSectionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing GuideSection instances.
    """

    list_display = ("guide_article", "section_type", "content")
    search_fields = ("guide_article__title", "section_type")
    list_filter = ("section_type",)
    inlines = [GuideSliderImageInline]

    def get_inline_instances(self, request, obj=None):
        """
        Override to conditionally include SliderImageInline based on obj's section_type.

        Args:
            request (HttpRequest): The current HTTP request.
            obj (BlogSection or None): The BlogSection instance being edited.

        Returns:
            list: List of inline instances to display.
        """
        if obj and obj.section_type == "slider":
            return [GuideSliderImageInline(self.model, self.admin_site)]
        return super().get_inline_instances(request, obj)

admin.site.register(GuideSection, GuideSectionAdmin)
