"""
ViewSet for managing EventDiscounts.
"""

from rest_framework import viewsets
from app.subscription.models.EventDiscount import EventDiscount
from app.subscription.serializers.EventDiscountSerializer import EventDiscountSerializer
from app.subscription.services.EventDiscountService import EventDiscountService
from rest_framework.decorators import action
class EventDiscountViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing EventDiscount instances.

    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` 
    actions for the EventDiscount model. It can be used to manage discount events 
    such as Black Friday, Eid, etc., where a percentage discount is applied to 
    subscription plans during a specified date range.
    """

    queryset = EventDiscount.objects.all()
    serializer_class = EventDiscountSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned discounts to a given start or end date,
        by filtering against `start_date` and `end_date` query parameters in the URL.
        """
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Retrieve a paginated list of EventDiscount objects.

        Uses the EventDiscountService to handle the retrieval and pagination
        of EventDiscount objects.

        Args:
            request (HttpRequest): The incoming HTTP request object.

        Returns:
            Response: A paginated response containing serialized EventDiscount objects
                or a 400 Bad Request response with an error message.
        """
        return EventDiscountService.event_discount_paginated(request)
    
    
    @action(detail=True, methods=["get"], url_path="get-active-discount", url_name="get-active-discount")
    def get_active_event_discount(self, request):
        """
        Retrieve EventDiscount objects with a start date greater than or equal to today.

        This method retrieves all EventDiscount objects from the database
        where the start date is greater than or equal to today's date.

        Returns:
            Response: A response containing serialized EventDiscount objects.
        """
        return EventDiscountService.get_active_event_discount()