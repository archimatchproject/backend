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

    Attributes:
        first_name (CharFilter): Filter by the first name of the related user.
        last_name (CharFilter): Filter by the last name of the related user.
        email (CharFilter): Filter by the email address of the related user.
        speciality_type (CharFilter): Filter by the label of the related speciality type.
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

    class Meta:
        """
        Meta class for SupplierFilter.

        This class defines the model and fields to be used in the SupplierFilter
        class. It specifies the Supplier model and the fields on which filtering
        can be applied. These fields include:
        - first_name: The first name of the related user.
        - last_name: The last name of the related user.
        - email: The email address of the related user.
        - speciality_type: The label of the related speciality type.

        Attributes:
            model (Supplier): The model to be filtered (Supplier model).
            fields (list of str): The list of fields on which filtering can be applied.
        """

        model = Supplier
        fields = ["first_name", "last_name", "email", "speciality_type","company_name","company_address"]
