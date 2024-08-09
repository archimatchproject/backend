"""
Module-level urls for project_core configuration.
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from project_core.env import env


schema_view = get_schema_view(
    openapi.Info(
        title="Archimatch API",
        default_version="v1",
        description="API description",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
)

URL_PREFIX = env("URL_PREFIX")

urlpatterns = [
    path(f"{URL_PREFIX}admin/", admin.site.urls),
    path(f"{URL_PREFIX}users/", include("app.users.urls")),
    path(f"{URL_PREFIX}cms/", include("app.cms.urls")),
    path(f"{URL_PREFIX}email_templates/", include("app.email_templates.urls")),
    path(
        f"{URL_PREFIX}announcement/",
        include("app.announcement.urls"),
    ),
    path(
        f"{URL_PREFIX}architect-request/",
        include("app.architect_request.urls"),
    ),
    path(
        f"{URL_PREFIX}architect-realization/",
        include("app.architect_realization.urls"),
    ),
    path(
        f"{URL_PREFIX}subscription/",
        include("app.subscription.urls"),
    ),
    path(
        f"{URL_PREFIX}catalogue/",
        include("app.catalogue.urls"),
    ),
    path(
        f"{URL_PREFIX}moderation/",
        include("app.moderation.urls"),
    ),
    path(
        f"{URL_PREFIX}swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        f"{URL_PREFIX}redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(f"{URL_PREFIX}rosetta/", include("rosetta.urls")),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
urlpatterns = [*i18n_patterns(*urlpatterns, prefix_default_language=False)]
