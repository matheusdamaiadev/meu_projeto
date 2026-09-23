from django.db import models
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Project, Task
from ..serializers import TaskSerializer
from .projects import ProjectPermission


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Task.objects.filter(
            models.Q(project__user=user)
            | models.Q(project__members__user=user)
        ).distinct()

        project_id = self.request.query_params.get("project")

        if project_id:
            queryset = queryset.filter(
                project_id=project_id
            )

        return queryset

    def perform_create(self, serializer):
        project_id = self.request.data.get("project")
        project = Project.objects.filter(id=project_id).first()

        if not project:
            raise NotFound("Projeto não encontrado.")

        permission = ProjectPermission()

        if not permission.can_edit(
            self.request,
            project
        ):
            raise PermissionDenied(
                "Você não tem permissão para criar tarefas neste projeto."
            )

        serializer.save(
            project=project
        )

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        permission = ProjectPermission()

        if not permission.can_edit(
            request,
            task.project
        ):
            return Response(
                {
                    "detail": "Você não tem permissão para editar tarefas."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(
            request,
            *args,
            **kwargs
        )

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        permission = ProjectPermission()

        if not permission.can_edit(
            request,
            task.project
        ):
            return Response(
                {
                    "detail": "Você não tem permissão para excluir tarefas."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(
            request,
            *args,
            **kwargs
        )