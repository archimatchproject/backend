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
from app.cms.routes.FAQQuestionUrls import faq_question_urlpatterns
from app.cms.routes.FAQThematicUrls import faq_thematic_urlpatterns
from app.cms.routes.GuideArticleUrls import guide_article_urlpatterns
from app.cms.routes.GuideThematicUrls import guide_thematic_urlpatterns
from app.cms.routes.PrivacyPolicyUrls import privacy_policy_urlpatterns
from app.cms.routes.TermsAndConditionsUrls import terms_and_conditions_urlpatterns
from app.cms.routes.CookiesPolicyUrls import cookies_policy_urlpatterns
from app.cms.routes.CGVCGUPolicyUrls import cgu_cgv_urlpatterns
router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    *blog_urlpatterns,
    *faq_thematic_urlpatterns,
    *guide_thematic_urlpatterns,
    *guide_article_urlpatterns,
    *blog_thematic_urlpatterns,
    *faq_question_urlpatterns,
    *privacy_policy_urlpatterns,
    *terms_and_conditions_urlpatterns,
    *cookies_policy_urlpatterns,
    *cgu_cgv_urlpatterns
]
