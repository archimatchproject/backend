from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.users.controllers.utils.IsSuperUser import IsSuperUser
from app.users.models import Supplier
from app.users.serializers import SupplierSerializer, UserAuthSerializer
from app.users.services import SupplierService


class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[],
        name="signup",
        serializer_class=UserAuthSerializer,
    )
    def signup(self, request):
        return SupplierService.supplier_signup(request)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[],
        name="login",
        serializer_class=UserAuthSerializer,
    )
    def login(self, request):
        return SupplierService.supplier_login(request)

    @action(
        detail=False, methods=["post"], permission_classes=[], name="first_connection"
    )
    def supplier_first_cnx(self, request):
        return SupplierService.supplier_first_connection(request)

    @action(
        detail=False, methods=["post"], permission_classes=[], name="update_profile"
    )
    def supplier_update_profile(self, request):
        return SupplierService.supplier_update_profile(request)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[],
        name="update_general_settings",
    )
    def supplier_update_general_settings(self, request):
        return SupplierService.supplier_update_general_settings(request)

    @action(detail=False, methods=["post"], permission_classes=[], name="update_links")
    def supplier_update_links(self, request):
        return SupplierService.supplier_update_links(request)
