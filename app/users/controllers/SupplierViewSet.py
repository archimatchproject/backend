from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from app.users.serializers import SupplierSerializer,UserAuthSerializer
from app.users.models import Supplier
from app.users.controllers.utils.IsSuperUser import IsSuperUser
from app.users.services import SupplierService 

class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    
    @action(detail=False, methods=['post'], permission_classes=[], name='signup',serializer_class=UserAuthSerializer)
    def signup(self, request):
        return SupplierService.signup(request)

    @action(detail=False, methods=['post'], permission_classes=[], name='login',serializer_class=UserAuthSerializer)
    def login(self, request):
        return SupplierService.login(request)
    
    @action(detail=False, methods=['post'], permission_classes=[], name='first-connection')
    def first_cnx(self, request):
        return SupplierService.first_connection(request)
    
    @action(detail=False, methods=['put'], permission_classes=[], name='update-profile')
    def update_profile(self, request):
        return SupplierService.update_profile(request)

    @action(detail=False, methods=['put'], name='update-bio')
    def update_bio(self, request):
        return SupplierService.update_bio(request)
    
    @action(detail=False, methods=['put'], name='update-presentation-video')
    def update_presentation_video(self, request):
        return SupplierService.update_presentation_video(request)

    @action(detail=False, methods=['put'], permission_classes=[], name='update-links')
    def update_links(self, request):
        return SupplierService.update_links(request)
