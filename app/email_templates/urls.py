"""
Module: app.urls

Description:
This module defines URL patterns for the Archimatch application using Django's path()
function.
It includes routing configurations for various API endpoints using Django Rest Framework's
DefaultRouter.

"""

from django.urls import path

from rest_framework import routers

from . import views


router = routers.DefaultRouter()


urlpatterns = [
    path("home/", views.home, name="home"),
]
