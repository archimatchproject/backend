from rest_framework import viewsets
from app.users.serializers import ClientSerializer,UserAuthSerializer,UserAuthPhoneSerializer
from app.users.models import Client
from rest_framework.decorators import action
from app.users.services import ClientService

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    

    @action(detail=False, methods=['post'], permission_classes=[], name='login',serializer_class=UserAuthSerializer)
    def login_email(self, request):
        return ClientService.client_login_email(request)
    
    @action(detail=False, methods=['post'], permission_classes=[], name='login',serializer_class=UserAuthPhoneSerializer)
    def login_phone(self, request):
        return ClientService.client_login_phone(request)

    
