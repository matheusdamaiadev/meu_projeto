from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ProjectSerializer,
    TaskSerializer
)

from .models import Project, Task


class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)


class ProjectViewSet(ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Project.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )

    def perform_update(self, serializer):

        project = self.get_object()

        new_is_pinned = serializer.validated_data.get(
            "is_pinned",
            project.is_pinned
        )

        if new_is_pinned and not project.is_pinned:

            pinned_count = Project.objects.filter(
                user=self.request.user,
                is_pinned=True
            ).count()

            if pinned_count >= 5:

                from rest_framework.exceptions import ValidationError

                raise ValidationError({
                    "is_pinned": "Você pode fixar no máximo 5 projetos."
                })

        serializer.save()


class TaskViewSet(ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Task.objects.filter(
            project__user=self.request.user
        )

        project_id = self.request.query_params.get("project")

        if project_id:
            queryset = queryset.filter(
                project_id=project_id
            )

        return queryset

    def perform_create(self, serializer):

        project = serializer.validated_data["project"]

        if project.user != self.request.user:

            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Você não pode criar uma tarefa neste projeto."
            )

        serializer.save()