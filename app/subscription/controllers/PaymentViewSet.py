"""
ViewSet module for the Payment model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.subscription.controllers.ManagePaymentPermission import ManagePaymentPermission
from app.subscription.models.Payment import Payment
from app.subscription.serializers.PaymentSerializer import PaymentSerializer
from app.subscription.services.PaymentService import PaymentService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Payment model.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        For `list` and `retrieve` actions (`GET` requests), no specific permissions are required.
        For `create`, `update`, `partial_update`, and `destroy` actions
        (`POST`, `PUT`, `PATCH`, `DELETE` requests),
        the view requires `IsAuthenticated` permissions.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["list", "retrieve", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), ManagePaymentPermission()]
        elif self.action in ["create", "get_payment_methods"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Override the create method to use PaymentService for handling the creation of a Payment.
        """
        success,data = PaymentService.create_architect_payment(request, request.data)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
        return 

    @action(detail=False, methods=["GET"])
    @handle_service_exceptions
    def get_payment_methods(self, request):
        """
        Return the payment methods from the choices.
        """
        success,data = PaymentService.get_payment_methods()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
