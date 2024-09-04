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

    def create(self, request, *args, **kwargs):
        """
        Override the create method to use PaymentService for handling the creation of a Payment.
        """
        return PaymentService.create_architect_payment(request, request.data)

    @action(detail=False, methods=["GET"])
    def get_payment_methods(self, request):
        """
        Return the payment methods from the choices.
        """
        return PaymentService.get_payment_methods()
