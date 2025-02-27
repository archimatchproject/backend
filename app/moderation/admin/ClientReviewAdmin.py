"""
Admin registration module for the ClientReview model.
"""

from django.contrib import admin

from app.moderation.models.ClientReview import ClientReview


class ClientReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for ClientReview.
    """

    list_display = ("architect", "client", "rating")
    search_fields = ("architect__user__email", "client__user__email", "rating")


admin.site.register(ClientReview, ClientReviewAdmin)
