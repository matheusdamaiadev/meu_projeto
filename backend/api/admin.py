from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "color",
        "icon",
        "created_at"
    )

    search_fields = (
        "name",
        "user__username"
    )

# Register your models here.
