from django.db import models
from django.contrib.auth.models import User
import random
import string


def generate_join_code():
    characters = string.ascii_uppercase + string.digits

    while True:
        code = "".join(
            random.choices(characters, k=4)
        )

        if not Project.objects.filter(join_code=code).exists():
            return code


class Project(models.Model):

    COLOR_CHOICES = [
        ("blue", "Azul"),
        ("green", "Verde"),
        ("purple", "Roxo"),
        ("orange", "Laranja"),
        ("red", "Vermelho"),
        ("yellow", "Amarelo"),
        ("gray", "Cinza"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default="blue"
    )

    icon = models.CharField(
        max_length=50,
        default="Folder"
    )

    is_pinned = models.BooleanField(
        default=False
    )

    join_code = models.CharField(
        max_length=4,
        unique=True,
        default=generate_join_code,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class ProjectMember(models.Model):

    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("viewer", "Visualizador"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="project_memberships"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="viewer"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "user"],
                name="unique_project_member"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"


class Task(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class Friendship(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("accepted", "Aceita"),
        ("rejected", "Recusada"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friendships_sent"
    )

    friend = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friendships_received"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "friend"],
                name="unique_friendship"
            )
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username}"


class Notification(models.Model):

    TYPE_CHOICES = [
        ("friend_request", "Solicitação de amizade"),
        ("project_invite", "Convite para projeto"),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=ProjectMember.ROLE_CHOICES,
        null=True,
        blank=True
    )

    read = models.BooleanField(
        default=False
    )

    accepted = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.type} - {self.recipient.username}"
