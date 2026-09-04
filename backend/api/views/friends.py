from django.contrib.auth.models import User
from django.db import models
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Friendship, Notification
from ..serializers import FriendshipSerializer, UserSerializer


class FriendSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get("username", "").strip()

        if not username:
            return Response([])

        users = User.objects.filter(username__icontains=username).exclude(
            id=request.user.id
        )[:20]

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class FriendListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friendships = (
            Friendship.objects.filter(status="accepted")
            .filter(
                models.Q(user=request.user) | models.Q(friend=request.user)
            )
            .select_related("user", "friend")
        )

        result = []
        added_users = set()

        for friendship in friendships:
            if friendship.user == request.user:
                other_user = friendship.friend
            else:
                other_user = friendship.user

            # Evita mostrar o mesmo amigo duas vezes
            # caso existam duas relações no banco.
            if other_user.id in added_users:
                continue

            added_users.add(other_user.id)

            result.append(
                {
                    "id": friendship.id,
                    "friend": other_user.id,
                    "username": other_user.username,
                    "status": friendship.status,
                    "created_at": friendship.created_at,
                }
            )

        return Response(result)


class FriendPendingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friendships = Friendship.objects.filter(
            user=request.user
        ).select_related("friend").order_by("-created_at")

        serializer = FriendshipSerializer(friendships, many=True)
        return Response(serializer.data)


class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get("username")

        if not username:
            return Response(
                {"detail": "Nome de usuário não informado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend = User.objects.filter(username=username).first()

        if not friend:
            return Response(
                {"detail": "Usuário não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if friend == request.user:
            return Response(
                {"detail": "Você não pode adicionar a si mesmo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing = Friendship.objects.filter(
            user=request.user, friend=friend
        ).first()
        reverse = Friendship.objects.filter(
            user=friend, friend=request.user
        ).first()

        if (existing and existing.status == "accepted") or (
            reverse and reverse.status == "accepted"
        ):
            return Response(
                {"detail": "Vocês já são amigos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if existing and existing.status == "pending":
            return Response(
                {"detail": "Solicitação já enviada. Aguarde a resposta."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if reverse and reverse.status == "pending":
            return Response(
                {
                    "detail": "Este usuário já enviou uma solicitação para você."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if existing and existing.status == "rejected":
            existing.status = "pending"
            existing.save(update_fields=["status"])

            Friendship.objects.filter(user=friend, friend=request.user).delete()
            friendship = existing
        else:
            friendship = Friendship.objects.create(
                user=request.user, friend=friend, status="pending"
            )

        Notification.objects.create(
            recipient=friend, sender=request.user, type="friend_request"
        )

        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FriendAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, friendship_id):
        friendship = Friendship.objects.filter(
            id=friendship_id, friend=request.user, status="pending"
        ).first()

        if not friendship:
            return Response(
                {"detail": "Solicitação não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        friendship.status = "accepted"
        friendship.save(update_fields=["status"])

        reverse = Friendship.objects.filter(
            user=request.user, friend=friendship.user
        ).first()

        if reverse:
            reverse.status = "accepted"
            reverse.save(update_fields=["status"])
        else:
            Friendship.objects.create(
                user=request.user, friend=friendship.user, status="accepted"
            )

        Notification.objects.filter(
            recipient=request.user,
            sender=friendship.user,
            type="friend_request",
            read=False,
        ).update(read=True, accepted=True)

        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)


class FriendRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, friendship_id):
        friendship = Friendship.objects.filter(
            id=friendship_id, friend=request.user, status="pending"
        ).first()

        if not friendship:
            return Response(
                {"detail": "Solicitação não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        friendship.status = "rejected"
        friendship.save(update_fields=["status"])

        Notification.objects.filter(
            recipient=request.user,
            sender=friendship.user,
            type="friend_request",
            read=False,
        ).update(read=True)

        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)


class FriendDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, friendship_id):
        friendship = Friendship.objects.filter(
            id=friendship_id, status="accepted"
        ).first()

        if not friendship:
            raise NotFound("Amizade não encontrada.")

        if (
            friendship.user != request.user
            and friendship.friend != request.user
        ):
            raise PermissionDenied("Você não pode remover esta amizade.")

        Friendship.objects.filter(
            user=friendship.user, friend=friendship.friend
        ).delete()
        Friendship.objects.filter(
            user=friendship.friend, friend=friendship.user
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
