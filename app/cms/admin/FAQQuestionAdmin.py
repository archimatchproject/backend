"""
Module defining the FAQQuestionAdmin and related configurations.

This module contains the admin configuration for the FAQQuestion model,
providing customization options for managing FAQ entries.
"""

from django.contrib import admin

from app.cms.models.FAQQuestion import FAQQuestion


class FAQQuestionAdmin(admin.ModelAdmin):
    """
    Admin descriptor for FAQQuestion model.
    """

    list_display = ("question", "faq_thematic")
    search_fields = ("question", "faq_thematic__title")
    list_filter = ("faq_thematic",)


admin.site.register(FAQQuestion, FAQQuestionAdmin)
