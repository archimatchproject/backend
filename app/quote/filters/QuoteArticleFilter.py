"""
This module defines a filter class for filtering QuoteArticle objects based on their title.
"""

import django_filters

from app.quote.models.QuoteArticle import QuoteArticle


class QuoteArticleFilter(django_filters.FilterSet):
    """
    QuoteArticleFilter is a filter class for filtering QuoteArticle objects based on their title.
    title (django_filters.CharFilter): A filter for the title field of the QuoteArticle model,
    using case-insensitive containment lookup."""

    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        """
        Meta class for QuoteArticleFilter.
        Attributes:
            model (type): The model associated with this filter, which is QuoteArticle.
            fields (list): List of fields to include in the filter, in this case, ["title"].
        """

        model = QuoteArticle
        fields = ["title"]
