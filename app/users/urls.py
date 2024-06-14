from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenRefreshView
from app.users.controllers import (AdminViewSet,ClientViewSet,SupplierViewSet,ArchimatchUserViewSet,ArchimatchUserObtainPairView)
router = routers.DefaultRouter()
router.register('admin', AdminViewSet, basename='admin')
router.register('client',ClientViewSet,basename='client')
router.register('supplier',SupplierViewSet,basename='supplier')
router.register('archimatch-user', ArchimatchUserViewSet, basename='archimatch-user')

urlpatterns = [
    path("", include(router.urls)),
    path("token/", ArchimatchUserObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
