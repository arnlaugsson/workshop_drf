from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth

from rest_framework import serializers

from . import models


class Task(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        'task-detail', source='id', read_only=True)
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)
    categories = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.Category.objects.all(),
        many=True)
    responsible = serializers.SlugRelatedField(
            slug_field='username',
            queryset=auth.User.objects.all()
    )

    class Meta:
        model = models.Task
        fields = ('id', 'name', 'owner', 'categories', 'done', 'url', 'responsible')

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        task = models.Task.objects.create(**validated_data)
        task.categories = categories
        return task


class CategoryList(serializers.ModelSerializer):
    num_tasks = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'num_tasks')

    def get_num_tasks(self, obj):
        return obj.tasks.count()


class CategoryDetail(CategoryList):
    tasks = Task(many=True, read_only=True)

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'num_tasks', 'tasks')


class MyCategory(serializers.ModelSerializer):
    tasks = Task(many=True, source='my_tasks')
    class Meta:
        model = models.Category
        fields = ('id', 'name', 'tasks')


class User(serializers.ModelSerializer):
    users = auth.User()
    
    class Meta:
        model = auth.User
        fields = ('username', 'email')
