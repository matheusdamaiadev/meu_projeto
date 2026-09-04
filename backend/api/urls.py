from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    MeView,
    ProjectViewSet,
    TaskViewSet,
    EmailTokenObtainPairView,
)


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
        "token/",
        EmailTokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),

    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    path(
        "",
        include(router.urls)
    ),

]