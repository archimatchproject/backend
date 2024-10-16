import django_filters
from django.db.models import Q
from app.announcement.models.Announcement import Announcement
from django_filters import OrderingFilter

class AnnouncementFilter(django_filters.FilterSet):
    """
    FilterSet class for filtering Announcement instances based on related user fields,
    specialty type, and keywords.
    """

    property_type = django_filters.CharFilter(
        field_name="property_type__id", lookup_expr="icontains"
    )
    work_type = django_filters.CharFilter(
        field_name="work_type__id", lookup_expr="icontains"
    )
    
    city = django_filters.CharFilter(
        field_name="city", lookup_expr="icontains"
    )
    status = django_filters.CharFilter(method='filter_status')

    class Meta:
        model = Announcement
        fields = ["property_type", "work_type", "city", "status"]

    def filter_queryset(self, queryset):
        
        queryset = queryset.order_by('created_at') 
        return super().filter_queryset(queryset)

    def filter_status(self, queryset, name, value):
        
        statuses = [status.strip() for status in value.split(',')]
        
        if 'Accepted' in statuses:
            return queryset.filter(status='Accepted')
        elif any(status in statuses for status in ['Refused', 'Pending']):
            return queryset.exclude(status='Accepted')
        return queryset 