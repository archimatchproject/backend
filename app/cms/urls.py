"""
Module: app.urls

Description:
This module defines URL patterns for the Archimatch application using Django's path() function.
It includes routing configurations for various API endpoints using Django Rest Framework's
DefaultRouter.

"""

from django.urls import include
from django.urls import path

from rest_framework import routers

from app.cms.routes.BlogThematicUrls import blog_thematic_urlpatterns
from app.cms.routes.BlogUrls import blog_urlpatterns
from app.cms.routes.FAQThematicUrls import faq_thematic_urlpatterns
from app.cms.routes.GuideArticleUrls import guide_article_urlpatterns
from app.cms.routes.GuideThematicUrls import guide_thematic_urlpatterns


router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    *blog_urlpatterns,
    *faq_thematic_urlpatterns,
    *guide_thematic_urlpatterns,
    *guide_article_urlpatterns,
    *blog_thematic_urlpatterns,
]
