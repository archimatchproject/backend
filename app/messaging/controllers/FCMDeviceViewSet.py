"""
CustomFCMDeviceViewSet is a subclass of FCMDeviceViewSet that enforces
authentication using the IsAuthenticated permission class.
This view set is used to manage FCM (Firebase Cloud Messaging) devices
registered in the system.
Attributes:
    permission_classes (list): A list of permission classes that are used
    to determine if a user is authenticated. In this case, it uses
    IsAuthenticated to ensure that only authenticated users can access
    the view set.
"""

from fcm_django.api.rest_framework import FCMDeviceViewSet
from rest_framework.permissions import IsAuthenticated


class CustomFCMDeviceViewSet(FCMDeviceViewSet):
    """
    Custom view set for handling FCM (Firebase Cloud Messaging) device registrations.
    This view set extends the FCMDeviceViewSet and applies the following customizations:
    - Requires the user to be authenticated to access the endpoints.
    Attributes:
        permission_classes (list): List of permission classes that are applied to the view set.
                                   In this case, it ensures that only authenticated users can access the endpoints.
    """

    permission_classes = [IsAuthenticated]
