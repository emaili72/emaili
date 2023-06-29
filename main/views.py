from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import *
from .models import *

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

class CategoryViewSet(ModelViewSet):
    queryset  = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('q',openapi.IN_QUERY, type=openapi.TYPE_STRING)
    ])
    @action(['GET'], detail=False)
    def search(self,requests):
        q = requests.query_params.get('q')
        queryset = self.get_queryset()
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(body__icontains=q))
        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializers = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializers.data)
        serializers = self.get_serializer(queryset, many=True)
        return Response(serializers.data, status=200)
