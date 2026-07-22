from django.db import models
from django.contrib.auth.models import User


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


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return self.name