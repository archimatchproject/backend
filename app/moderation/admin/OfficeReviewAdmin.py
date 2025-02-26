"""
Admin configuration for the OfficeReview model.
This module defines the admin interface for managing OfficeReview objects in the Django admin.
"""

from django.contrib import admin

from app.moderation.models import OfficeReview


class OfficeReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for OfficeReview.
    """

    list_display = ("architect", "office", "rating", "comment")
    list_filter = ("rating",)
    search_fields = ("architect__user__email", "office__office_name")
    ordering = ("-created_at",)


admin.site.register(OfficeReview, OfficeReviewAdmin)
