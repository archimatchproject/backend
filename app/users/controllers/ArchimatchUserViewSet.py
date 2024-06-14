
from app.users.serializers import ArchimatchUserSerializer,ArchimatchUserCreatePWSerializer
from app.users.serializers.utils.ArchimatchUserObtainPairSerializer import ArchimatchUserObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework.decorators import action
from app.users.services import ArchimatchUserService
from app.users.models import ArchimatchUser
from rest_framework.exceptions import MethodNotAllowed



    
class ArchimatchUserObtainPairView(TokenObtainPairView):
    serializer_class = ArchimatchUserObtainPairSerializer



class ArchimatchUserViewSet(viewsets.ModelViewSet):
    queryset = ArchimatchUser.objects.all()
    serializer_class = ArchimatchUserSerializer
    
    def list(self, request, *args, **kwargs): 
        raise MethodNotAllowed("GET") 
    def retrieve(self, request, *args, **kwargs): 
        raise MethodNotAllowed("GET") 
    def create(self, request, *args, **kwargs): 
        raise MethodNotAllowed("POST") 
    def update(self, request, *args, **kwargs): 
        raise MethodNotAllowed("PUT") 
    def partial_update(self, request, *args, **kwargs): 
        raise MethodNotAllowed("PATCH") 
    def destroy(self, request, *args, **kwargs): 
        raise MethodNotAllowed("DELETE")
    
    @action(detail=False, methods=['post'], url_path='create-password',serializer_class=ArchimatchUserCreatePWSerializer)
    def create_password(self, request):
        return ArchimatchUserService.create_password(request)