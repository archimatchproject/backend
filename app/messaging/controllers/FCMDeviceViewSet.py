from fcm_django.models import FCMDevice
from fcm_django.api.rest_framework import FCMDeviceViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class CustomFCMDeviceViewSet(FCMDeviceViewSet):
    permission_classes = [IsAuthenticated]

