from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from app.users.serializers import AdminSerializer,UserAuthSerializer
from app.users.models import Admin
from .utils import IsSuperUser
from app.users.services import AdminService 

class AdminViewSet(viewsets.ModelViewSet):
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()
    permission_classes = [IsSuperUser]
    

    def create(self, request, *args, **kwargs):
        return AdminService.create_admin(request.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        return AdminService.update_admin(instance, request.data)

    @action(detail=False, methods=['post'], permission_classes=[], name='retrieve_by_token')
    def retrieve_by_token(self, request):
        return AdminService.retrieve_by_token(request)

    @action(detail=False, methods=['post'], permission_classes=[], name='login',serializer_class=UserAuthSerializer)
    def login(self, request):
        return AdminService.admin_login(request)
