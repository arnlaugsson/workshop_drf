from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response

from . import serializers, models, filters


class Category(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CategoryList
        return serializers.CategoryDetail

    @detail_route()
    def mine(self, request, *args, **kwargs):
        category = self.get_object()
        category.my_tasks = category.tasks.filter(owner=request.user)
        serializer = serializers.MyCategory(
                category,
                context={'request': request}
        )
        return Response(serializer.data)


class Task(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.Task
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.Task

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @list_route()
    def mine(self, request):
        queryset = self.filter_queryset(
                self.get_queryset().filter(owner=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def assigned(self, request):
        queryset = self.filter_queryset(
            self.get_queryset().filter(responsible=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class User(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.User
