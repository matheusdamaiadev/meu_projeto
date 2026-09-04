from django.contrib.auth.models import User

from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Project, Task


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate_username(self, value):

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Este nome de usuário já está sendo usado."
            )

        return value

    def validate_email(self, value):

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Este email já está sendo usado."
            )

        return value

    def create(self, validated_data):

        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email"]


class EmailTokenObtainPairSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        email = attrs["email"]
        password = attrs["password"]

        try:
            user = User.objects.get(email__iexact=email)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Email ou senha incorretos."}
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                {"email": "Email ou senha incorretos."}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"email": "Esta conta está desativada."}
            )

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


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