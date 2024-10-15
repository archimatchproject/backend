"""
Module: Supplier Filters

This module defines the filter classes used to filter Supplier instances
based on various criteria related to the user and other related fields.
It uses the django_filters library to facilitate the filtering process.

Classes:
    SupplierFilter: FilterSet class for filtering Supplier instances based on related
    user fields and speciality type.
"""

import django_filters
from django.db.models import Q

from app.users.models.Supplier import Supplier

class SupplierFilter(django_filters.FilterSet):
    """
    FilterSet class for filtering Supplier instances based on related user fields
    and speciality type.

    This class allows filtering of Supplier objects based on the following fields:
    - First Name: Filters suppliers by the first name of the related user using
      a case-insensitive contains lookup.
    - Last Name: Filters suppliers by the last name of the related user using
      a case-insensitive contains lookup.
    - Email: Filters suppliers by the email address of the related user using
      a case-insensitive contains lookup.
    - Speciality Type: Filters suppliers by the label of the related speciality type
      using a case-insensitive contains lookup.
    - Company Name Existence: Filters suppliers based on whether the company_name
      is empty or not.
    """

    first_name = django_filters.CharFilter(field_name="user__first_name", lookup_expr="icontains")
    last_name = django_filters.CharFilter(field_name="user__last_name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="user__email", lookup_expr="icontains")
    speciality_type = django_filters.CharFilter(
        field_name="speciality_type__id", lookup_expr="icontains"
    )
    company_name = django_filters.CharFilter(
        field_name="company_name", lookup_expr="icontains"
    )
    company_address = django_filters.CharFilter(
        field_name="company_address", lookup_expr="icontains"
    )
    
    company_name_exists = django_filters.BooleanFilter(method='filter_company_name_exists')

    class Meta:
        """
        Meta class for SupplierFilter.
        """
        model = Supplier
        fields = [
            "first_name", "last_name", "email",
            "speciality_type", "company_name", "company_address",
            "company_name_exists"
        ]
    def filter_queryset(self, queryset):
        
        queryset = queryset.order_by('created_at') 
        return super().filter_queryset(queryset)
  
    def filter_company_name_exists(self, queryset, name, value):
        """
        Custom filter method to filter suppliers based on the existence of company_name.
        If value is True, include suppliers with non-empty company_name.
        If value is False, include suppliers with empty company_name.
        """
        if value:
            return queryset.exclude(company_name='')
        return queryset.filter(company_name='')