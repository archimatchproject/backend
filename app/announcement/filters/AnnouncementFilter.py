import django_filters
from django.db.models import Q
from app.announcement.models.Announcement import Announcement


class AnnouncementFilter(django_filters.FilterSet):
    """
    FilterSet class for filtering Announcement instances based on related user fields,
    speciality type, and keywords.
    """

    property_type = django_filters.CharFilter(
        field_name="property_type__id", lookup_expr="icontains"
    )
    work_type = django_filters.CharFilter(
        field_name="work_type__id", lookup_expr="icontains"
    )
    
    address = django_filters.CharFilter(
        field_name="address", lookup_expr="icontains"
    )

    class Meta:
        model = Announcement
        fields = ["property_type", "work_type","address"]
