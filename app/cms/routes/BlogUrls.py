"""
exposed URLS for cms app
viewset : BlogViewSet
"""

from django.urls import path

from app.cms.controllers.BlogViewSet import BlogViewSet


blog_urlpatterns = [
    path(
        "blog/get-blogs/",
        BlogViewSet.as_view({"get": "get_blogs"}),
        name="get-blogs",
    ),
]
