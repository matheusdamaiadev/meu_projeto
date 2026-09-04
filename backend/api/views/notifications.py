from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Notification
from ..serializers import NotificationSerializer


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = (
            Notification.objects.filter(recipient=request.user)
            .select_related("sender", "project")
            .order_by("-created_at")
        )

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class NotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        notification = Notification.objects.filter(
            id=notification_id, recipient=request.user
        ).first()

        if not notification:
            return Response(
                {"detail": "Notificação não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        notification.read = True
        notification.save(update_fields=["read"])

        serializer = NotificationSerializer(notification)
        return Response(serializer.data)
