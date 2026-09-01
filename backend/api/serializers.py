from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Project, Task


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password',
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            "username",
            "email",
        ]


class ProjectSerializer(serializers.ModelSerializer):

    task_count = serializers.SerializerMethodField()

    completed_task_count = serializers.SerializerMethodField()

    class Meta:

        model = Project

        fields = [
            "id",
            "name",
            "description",
            "color",
            "icon",
            "is_pinned",
            "task_count",
            "completed_task_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "task_count",
            "completed_task_count",
            "created_at",
            "updated_at",
        ]

    def get_task_count(self, obj):

        return obj.tasks.count()

    def get_completed_task_count(self, obj):

        return obj.tasks.filter(
            completed=True
        ).count()


class TaskSerializer(serializers.ModelSerializer):

    class Meta:

        model = Task

        fields = [
            "id",
            "project",
            "title",
            "description",
            "completed",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]