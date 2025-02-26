"""
This module defines a filter class for filtering QuoteServices objects based on their title.
"""

import django_filters

from app.quote.models.QuoteService import QuoteService


class QuoteServiceFilter(django_filters.FilterSet):
    """
    QuoteServiceFilter is a filter class for filtering QuoteService objects based on specified fields.
        title (django_filters.CharFilter): Filter for the 'title' field of the QuoteService model, using
        case-insensitive containment lookup.
        category (django_filters.CharFilter): Filter for the 'category__id' field of the QuoteService model,
        using case-insensitive containment lookup.
    Meta:
        model (type): The model class that this filter is based on, which is QuoteService.
        fields (list): List of fields to include in the filter, which are 'title' and 'category'.
    """

    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    category = django_filters.CharFilter(field_name="category__id", lookup_expr="icontains")

    class Meta:
        """
        Meta class for QuoteServiceFilter.
        Attributes:
            model (type): The model class that this filter is based on.
            fields (list): List of fields to include in the filter.
        """

        model = QuoteService
        fields = ["title", "category"]
