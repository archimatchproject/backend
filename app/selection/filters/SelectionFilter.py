import django_filters
from django.db.models import Q
from app.selection.models.Selection import Selection
from django_filters import OrderingFilter

class SelectionFilter(django_filters.FilterSet):
    """
    FilterSet class for filtering Selection instances based on related  fields,

    """

    status = django_filters.CharFilter(
        field_name="status", lookup_expr="icontains"
    )
    
    class Meta:
        model = Selection
        fields = ["status"]

    