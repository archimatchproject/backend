"""
Module defining the FAQThematicAdmin and related configurations.

This module contains the admin configuration for the FAQThematic model,
including an inline configuration for related FAQQuestion entries.
"""

from django.contrib import admin

from app.cms.models.FAQQuestion import FAQQuestion
from app.cms.models.FAQThematic import FAQThematic


class FAQQuestionInline(admin.TabularInline):
    """
    Inline admin descriptor for FAQQuestion model.
    This will display FAQQuestion entries as inline forms within the FAQThematic admin page.
    """

    model = FAQQuestion
    extra = 3
    fields = ("question", "response", "guide_thematic", "guide_article", "admin")


class FAQThematicAdmin(admin.ModelAdmin):
    """
    Admin descriptor for FAQThematic model.
    """

    list_display = ("title",)
    search_fields = ("title",)
    inlines = [FAQQuestionInline]


admin.site.register(FAQThematic, FAQThematicAdmin)
