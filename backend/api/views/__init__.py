from .auth import EmailTokenObtainPairView, MeView, RegisterView
from .friends import (
    FriendAcceptView,
    FriendDeleteView,
    FriendListView,
    FriendPendingView,
    FriendRejectView,
    FriendRequestView,
    FriendSearchView,
)
from .notifications import NotificationListView, NotificationReadView
from .projects import (
    JoinProjectView,
    ProjectMembersView,
    ProjectPermission,
    ProjectViewSet,
)
from .tasks import TaskViewSet
