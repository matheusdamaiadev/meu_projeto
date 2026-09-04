from django.contrib.auth.models import User
from django.db import models
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Project, ProjectMember
from ..serializers import ProjectMemberSerializer, ProjectSerializer


class ProjectPermission:
    def has_permission(self, request, project):
        if project.user == request.user:
            return True

        membership = ProjectMember.objects.filter(
            project=project, user=request.user
        ).first()

        return membership is not None

    def can_edit(self, request, project):
        if project.user == request.user:
            return True

        membership = ProjectMember.objects.filter(
            project=project, user=request.user
        ).first()

        if not membership:
            return False

        return membership.role == "admin"


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            models.Q(user=user) | models.Q(members__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        permission = ProjectPermission()

        if not permission.can_edit(request, project):
            return Response(
                {"detail": "Você não tem permissão para editar este projeto."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        if project.user != request.user:
            return Response(
                {"detail": "Apenas o proprietário pode excluir o projeto."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, *args, **kwargs)


class JoinProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get("join_code")

        if not code:
            return Response(
                {"detail": "Código do projeto não informado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        code = code.upper()
        project = Project.objects.filter(join_code=code).first()

        if not project:
            return Response(
                {"detail": "Projeto não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if project.user == request.user:
            return Response(
                {"detail": "Você já é o proprietário deste projeto."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member = ProjectMember.objects.filter(
            project=project, user=request.user
        ).first()

        if member:
            return Response(
                {"detail": "Você já participa deste projeto."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member = ProjectMember.objects.create(
            project=project, user=request.user, role="viewer"
        )

        serializer = ProjectMemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def get_project(self, project_id):
        return Project.objects.filter(id=project_id).first()

    def get(self, request, project_id):
        project = self.get_project(project_id)

        if not project:
            return Response(
                {"detail": "Projeto não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        permission = ProjectPermission()
        if not permission.has_permission(request, project):
            return Response(
                {"detail": "Você não participa deste projeto."},
                status=status.HTTP_403_FORBIDDEN,
            )

        members = ProjectMember.objects.filter(project=project).select_related(
            "user"
        )
        serializer = ProjectMemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        project = self.get_project(project_id)

        if not project:
            return Response(
                {"detail": "Projeto não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        permission = ProjectPermission()
        if not permission.can_edit(request, project):
            return Response(
                {"detail": "Você não tem permissão para gerenciar membros."},
                status=status.HTTP_403_FORBIDDEN,
            )

        username = request.data.get("username")
        role = request.data.get("role", "viewer")

        if role not in ["admin", "viewer"]:
            return Response(
                {"detail": "Função inválida."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(username=username).first()

        if not user:
            return Response(
                {"detail": "Usuário não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user == project.user:
            return Response(
                {"detail": "O proprietário já faz parte do projeto."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing = ProjectMember.objects.filter(
            project=project, user=user
        ).first()

        if existing:
            return Response(
                {"detail": "Este usuário já participa do projeto."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member = ProjectMember.objects.create(
            project=project, user=user, role=role
        )

        serializer = ProjectMemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, project_id, member_id):
        project = self.get_project(project_id)

        if not project:
            return Response(
                {"detail": "Projeto não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        permission = ProjectPermission()
        if not permission.can_edit(request, project):
            return Response(
                {"detail": "Você não tem permissão para gerenciar membros."},
                status=status.HTTP_403_FORBIDDEN,
            )

        member = ProjectMember.objects.filter(
            id=member_id, project=project
        ).first()

        if not member:
            return Response(
                {"detail": "Membro não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        role = request.data.get("role")
        if role not in ["admin", "viewer"]:
            return Response(
                {"detail": "Função inválida."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member.role = role
        member.save(update_fields=["role"])

        serializer = ProjectMemberSerializer(member)
        return Response(serializer.data)

    def delete(self, request, project_id, member_id):
        project = self.get_project(project_id)

        if not project:
            return Response(
                {"detail": "Projeto não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        permission = ProjectPermission()
        if not permission.can_edit(request, project):
            return Response(
                {"detail": "Você não tem permissão para gerenciar membros."},
                status=status.HTTP_403_FORBIDDEN,
            )

        member = ProjectMember.objects.filter(
            id=member_id, project=project
        ).first()

        if not member:
            return Response(
                {"detail": "Membro não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
