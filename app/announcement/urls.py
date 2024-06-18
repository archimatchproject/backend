from django.urls import path, include
from rest_framework import routers
from app.announcement.controllers import AnnouncementViewSet


router = routers.DefaultRouter()
router.register('announcement', AnnouncementViewSet,basename='announcement')

urlpatterns = [
    path("", include(router.urls)),
    
]
