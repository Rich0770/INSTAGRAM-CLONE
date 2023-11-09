from rest_framework import generics
from django.shortcuts import render
from rest_framework.permissions import AllowAny

from post.models import Post
from post.serializers import PostSerializer
from shared.pagination import CustomPagination

class PostListApiView(generics.ListAPIView):
    permission_class = [AllowAny,]
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()
