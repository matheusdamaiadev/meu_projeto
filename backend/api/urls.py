from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import RegisterView, MeView, ProjectViewSet, TaskViewSet


router = DefaultRouter()

router.register(
    "projects",
    ProjectViewSet,
    basename="projects"
)

router.register(
    "tasks",
    TaskViewSet,
    basename="tasks"
)


urlpatterns = [

    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "me/",
        MeView.as_view(),
        name="me"
    ),

    path(
        "",
        include(router.urls)
    ),

]