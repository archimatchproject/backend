from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.cms.models import Blog
from app.cms.serializers import BlogSerializer
from app.cms.controllers.utils.ManageBlogPermission import ManageBlogPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated,ManageBlogPermission]

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny], name='get_blogs')
    def get_blogs(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)