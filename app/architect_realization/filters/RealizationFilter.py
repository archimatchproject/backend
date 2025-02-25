"""
This module defines custom filters for the Realization model in the Django application.
Classes:
    MultipleValueFilter: A custom filter that can accept either a single value or a comma-separated list of values.
    RealizationFilter: A FilterSet class for filtering Realization instances based on related user fields,
Methods:
    MultipleValueFilter.filter(qs, value): Filters the queryset based on a single value or a comma-separated list
    of values.
    RealizationFilter.filter_by_keyword(queryset, name, value): Custom filter method to search the given keyword across
    multiple fields.
"""

from django.db.models import Q

import django_filters

from app.architect_realization.models.Realization import Realization


class MultipleValueFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """
    Custom filter that can accept either a single value or a comma-separated list of values.
    """

    def filter(self, qs, value):
        """
        Filters the queryset based on the provided value.
        Args:
            qs (QuerySet): The initial queryset to be filtered.
            value (str or list): The value to filter the queryset by. If a string is provided,
                                 it will be split by commas into a list of values.
        Returns:
            QuerySet: The filtered queryset. If no value is provided, the original queryset is returned.
        """

        if not value:
            return qs
        if isinstance(value, str):
            value = value.split(",")
        return super().filter(qs, value)


class RealizationFilter(django_filters.FilterSet):
    """
    FilterSet class for filtering Realization instances based on related user fields,
    speciality type, and keywords.
    """

    property_type = MultipleValueFilter(field_name="property_type__id", lookup_expr="in")
    project_category = MultipleValueFilter(field_name="project_category__id", lookup_expr="in")
    keyword = django_filters.CharFilter(method="filter_by_keyword")

    class Meta:
        """
        Meta class for specifying the model and fields to be used in the filter.
        Attributes:
            model (type): The model class to be used in the filter.
            fields (list): A list of field names to be included in the filter.
        """

        model = Realization
        fields = ["property_type", "project_category"]

    def filter_by_keyword(self, queryset, name, value):
        """
        Custom filter method to search the given keyword across multiple fields.

        Args:
            queryset (QuerySet): The initial queryset.
            name (str): The name of the filter field.
            value (str): The keyword value to filter by.

        Returns:
            QuerySet: The filtered queryset.
        """
        keywords = value.split()

        query = Q()
        for keyword in keywords:
            query |= (
                Q(project_name__icontains=keyword)
                | Q(address__icontains=keyword)
                | Q(city__icontains=keyword)
                | Q(work_surface__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(architect__user__first_name__icontains=keyword)
                | Q(architect__architect_speciality__label__icontains=keyword)
                | Q(architectural_style__label__icontains=keyword)
            )
        return queryset.filter(query).distinct()
