from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    EmailTokenObtainPairView,
    FriendAcceptView,
    FriendDeleteView,
    FriendListView,
    FriendPendingView,
    FriendRejectView,
    FriendRequestView,
    FriendSearchView,
    JoinProjectView,
    MeView,
    NotificationListView,
    NotificationReadView,
    ProjectMembersView,
    ProjectViewSet,
    RegisterView,
    TaskViewSet,
)

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="projects")
router.register("tasks", TaskViewSet, basename="tasks")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("projects/join/", JoinProjectView.as_view(), name="project-join"),
    path(
        "projects/<int:project_id>/members/",
        ProjectMembersView.as_view(),
        name="project-members",
    ),
    path(
        "projects/<int:project_id>/members/<int:member_id>/",
        ProjectMembersView.as_view(),
        name="project-member-detail",
    ),
    path("token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ========================================================
    # AMIZADES
    # ========================================================
    path("friends/", FriendListView.as_view(), name="friends"),
    path("friends/search/", FriendSearchView.as_view(), name="friend-search"),
    path("friends/pending/", FriendPendingView.as_view(), name="friend-pending"),
    path("friends/request/", FriendRequestView.as_view(), name="friend-request"),
    path(
        "friends/<int:friendship_id>/accept/",
        FriendAcceptView.as_view(),
        name="friend-accept",
    ),
    path(
        "friends/<int:friendship_id>/reject/",
        FriendRejectView.as_view(),
        name="friend-reject",
    ),
    path(
        "friends/<int:friendship_id>/",
        FriendDeleteView.as_view(),
        name="friend-delete",
    ),
    # ========================================================
    # NOTIFICAÇÕES
    # ========================================================
    path(
        "notifications/",
        NotificationListView.as_view(),
        name="notifications",
    ),
    path(
        "notifications/<int:notification_id>/read/",
        NotificationReadView.as_view(),
        name="notification-read",
    ),
    path("", include(router.urls)),
]
