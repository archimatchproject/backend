from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.cms.controllers.utils.ManageBlogPermission import ManageBlogPermission
from app.cms.models import Blog
from app.cms.serializers import BlogSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated, ManageBlogPermission]

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.AllowAny],
        name="get_blogs",
    )
    def get_blogs(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
