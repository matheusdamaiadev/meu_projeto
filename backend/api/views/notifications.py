from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Notification, ProjectMember
from ..serializers import NotificationSerializer, ProjectMemberSerializer


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = (
            Notification.objects.filter(
                recipient=request.user
            )
            .select_related("sender", "project")
            .order_by("-created_at")
        )

        serializer = NotificationSerializer(
            notifications,
            many=True
        )

        return Response(serializer.data)


class NotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        notification = Notification.objects.filter(
            id=notification_id,
            recipient=request.user,
        ).first()

        if not notification:
            return Response(
                {"detail": "Notificação não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        notification.read = True

        notification.save(
            update_fields=["read"]
        )

        serializer = NotificationSerializer(
            notification
        )

        return Response(serializer.data)


class ProjectInviteResponseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        action = request.data.get("action")

        if action not in ["accept", "reject"]:
            return Response(
                {
                    "detail": (
                        "Ação inválida. "
                        "Use 'accept' ou 'reject'."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        notification = (
            Notification.objects.filter(
                id=notification_id,
                recipient=request.user,
                type="project_invite",
                read=False,
                accepted=False,
            )
            .select_related("project")
            .first()
        )

        if not notification:
            return Response(
                {
                    "detail": (
                        "Convite não encontrado "
                        "ou já respondido."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not notification.project:
            return Response(
                {
                    "detail": (
                        "O projeto deste convite "
                        "não existe mais."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =========================
        # RECUSAR CONVITE
        # =========================

        if action == "reject":
            notification.read = True
            notification.accepted = False

            notification.save(
                update_fields=[
                    "read",
                    "accepted",
                ]
            )

            serializer = NotificationSerializer(
                notification
            )

            return Response(serializer.data)

        # =========================
        # ACEITAR CONVITE
        # =========================

        existing_member = ProjectMember.objects.filter(
            project=notification.project,
            user=request.user,
        ).first()

        if existing_member:
            notification.read = True
            notification.accepted = True

            notification.save(
                update_fields=[
                    "read",
                    "accepted",
                ]
            )

            return Response(
                {
                    "detail": (
                        "Você já participa "
                        "deste projeto."
                    ),
                    "member": ProjectMemberSerializer(
                        existing_member
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        member = ProjectMember.objects.create(
            project=notification.project,
            user=request.user,
            role=notification.role or "viewer",
        )

        notification.read = True
        notification.accepted = True

        notification.save(
            update_fields=[
                "read",
                "accepted",
            ]
        )

        return Response(
            {
                "detail": (
                    "Convite aceito com sucesso."
                ),
                "member": ProjectMemberSerializer(
                    member
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )
