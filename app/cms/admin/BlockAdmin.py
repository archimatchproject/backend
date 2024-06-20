"""
Django admin configuration for managing CMS blocks and slider images.

This module defines admin classes and inlines for managing Block and SliderImage models
in the Django admin interface.
"""

from django.contrib import admin

from app.cms.models import Block, SliderImage


class SliderImageInline(admin.TabularInline):
    """
    Inline admin configuration for SliderImage model.

    This inline admin class allows managing SliderImage instances within the BlockAdmin.
    """

    model = SliderImage
    extra = 1


class BlockInline(admin.StackedInline):
    """
    Inline admin configuration for Block model with nested SliderImageInline.

    This inline admin class is used within BlockAdmin to manage Block instances,
    optionally with nested SliderImage instances based on block_type.
    """

    model = Block
    extra = 1
    inlines = [SliderImageInline]

    def get_inline_instances(self, request, obj=None):
        """
        Override to conditionally include SliderImageInline based on obj's block_type.

        Args:
            request (HttpRequest): The current HTTP request.
            obj (Block or None): The Block instance being edited.

        Returns:
            list: List of inline instances to display.
        """
        if obj and obj.block_type == "slider":
            return [SliderImageInline(self.model, self.admin_site)]
        return super().get_inline_instances(request, obj)


class BlockAdmin(admin.ModelAdmin):
    """
    Admin configuration for Block model.

    This admin class provides customizations for the Block model in the Django admin site.
    It includes list display fields, filters, and inline editing for associated SliderImage instances.
    """

    list_display = ("block_type", "blog", "content")
    list_filter = ("block_type", "blog")

    inlines = [SliderImageInline]

    def get_inline_instances(self, request, obj=None):
        """
        Override to conditionally include SliderImageInline based on obj's block_type.

        Args:
            request (HttpRequest): The current HTTP request.
            obj (Block or None): The Block instance being edited.

        Returns:
            list: List of inline instances to display.
        """
        if obj and obj.block_type == "slider":
            return [SliderImageInline(self.model, self.admin_site)]
        return super().get_inline_instances(request, obj)


admin.site.register(Block, BlockAdmin)
