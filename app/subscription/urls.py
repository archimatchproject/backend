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

from app.subscription.routes.InvoiceUrls import invoice_urlpatterns
from app.subscription.routes.PaymentUrls import payment_urlpatterns
from app.subscription.routes.PlanServiceUrls import plan_service_urlpatterns
from app.subscription.routes.SubscriptionPlanUrls import subscription_plan_urlpatterns
from app.subscription.routes.TokenPackUrls import token_pack_urlpatterns
from app.subscription.routes.SupplierSubscriptionPlanUrls import supplier_subscription_plan_urlpatterns
from app.subscription.routes.EventDiscountUrls import event_discount_urlpatterns

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    *plan_service_urlpatterns,
    *subscription_plan_urlpatterns,
    *token_pack_urlpatterns,
    *payment_urlpatterns,
    *invoice_urlpatterns,
    *supplier_subscription_plan_urlpatterns,
    *event_discount_urlpatterns
]
