"""
This module defines the `AnnouncementFilter` class, which is a Django FilterSet
used to filter `Announcement` instances based on various fields such as property type,
work type, city, and status.
Classes:
    AnnouncementFilter: A FilterSet class for filtering Announcement instances.
Filters:
    property_type (CharFilter): Filters announcements by property type ID using a case-insensitive match.
    work_type (CharFilter): Filters announcements by work type ID using a case-insensitive match.
    city (CharFilter): Filters announcements by city using a case-insensitive match.
    status (CharFilter): Filters announcements by status using a custom method.
Methods:
    filter_queryset(queryset): Orders the queryset by the `created_at` field before applying filters.
    filter_status(queryset, name, value): Custom filter method for filtering announcements by status.

"""

import django_filters

from app.announcement.models.Announcement import Announcement


class AnnouncementFilter(django_filters.FilterSet):
    """
    FilterSet class for filtering Announcement instances based on related user fields,
    specialty type, and keywords.
    """

    property_type = django_filters.CharFilter(field_name="property_type__id", lookup_expr="icontains")
    work_type = django_filters.CharFilter(field_name="work_type__id", lookup_expr="icontains")

    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    status = django_filters.CharFilter(method="filter_status")

    class Meta:
        """
        Meta class for AnnouncementFilter.
        Attributes:
            model (type): The model class that this filter is associated with.
            fields (list): A list of fields that can be used for filtering.
        """

        model = Announcement
        fields = ["property_type", "work_type", "city", "status"]

    def filter_queryset(self, queryset):
        """
        Filters and orders the given queryset by the 'created_at' field.
        Args:
            queryset (QuerySet): The initial queryset to be filtered and ordered.
        Returns:
            QuerySet: The filtered and ordered queryset.
        """

        queryset = queryset.order_by("created_at")
        return super().filter_queryset(queryset)

    def filter_status(self, queryset, name, value):
        """
        Filters the queryset based on the provided status values.
        Args:
            queryset (QuerySet): The initial queryset to filter.
            name (str): The name of the field to filter on (not used in this method).
            value (str): A comma-separated string of status values to filter by.
        Returns:
            QuerySet: The filtered queryset.
        Notes:
            - If "Accepted" is in the provided statuses, the queryset is filtered to include only "Accepted" statuses.
            - If "Refused" or "Pending" is in the provided statuses, the queryset is filtered to exclude "Accepted"
            statuses.
            - If none of the specified statuses are provided, the original queryset is returned.
        """

        statuses = [status.strip() for status in value.split(",")]

        if "Accepted" in statuses:
            return queryset.filter(status="Accepted")
        elif any(status in statuses for status in ["Refused", "Pending"]):
            return queryset.exclude(status="Accepted")
        return queryset
