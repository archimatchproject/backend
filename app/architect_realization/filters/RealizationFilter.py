import django_filters
from django.db.models import Q
from app.architect_realization.models.Realization import Realization


class MultipleValueFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """
    Custom filter that can accept either a single value or a comma-separated list of values.
    """

    def filter(self, qs, value):
        if not value:
            return qs
        if isinstance(value, str):
            value = value.split(',')
        return super().filter(qs, value)


class RealizationFilter(django_filters.FilterSet):
    """
    FilterSet class for filtering Realization instances based on related user fields,
    speciality type, and keywords.
    """

    property_type = MultipleValueFilter(
        field_name="property_type__id", lookup_expr="in"
    )
    project_category = MultipleValueFilter(
        field_name="project_category__id", lookup_expr="in"
    )
    keyword = django_filters.CharFilter(method='filter_by_keyword')

    class Meta:
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
                Q(project_name__icontains=keyword) |
                Q(address__icontains=keyword) |
                Q(city__icontains=keyword) |
                Q(work_surface__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(architect__user__first_name__icontains=keyword) |
                Q(architect__architect_speciality__label__icontains=keyword)|
                Q(architectural_style__label__icontains=keyword)
            )
        return queryset.filter(query).distinct()
