"""
Admin module for managing EventDiscount instances in the Django admin interface.
"""

from django.contrib import admin
from app.subscription.models.EventDiscount import EventDiscount


class EventDiscountAdmin(admin.ModelAdmin):
    """
    Admin class for managing EventDiscount instances.
    """

    list_display = ('event_name', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('event_name',)
    list_filter = ('start_date', 'end_date')
    ordering = ('start_date',)
    fields = ('event_name', 'discount_percentage', 'start_date', 'end_date')

admin.site.register(EventDiscount, EventDiscountAdmin)
