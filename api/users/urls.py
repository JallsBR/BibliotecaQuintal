from users.views.signin import Signin
from users.views.signup import Signup
from users.views.user import GetUser
from users.views.logout import Logout
from users.views.group import GroupListCreateView, GroupRetrieveUpdateDestroyView
from users.views.group_users import GroupUsersView
from users.views.permission import PermissionListView
from users.views.user_config import UserListView, UserRetrieveUpdateView
from rest_framework_simplejwt.views import ( TokenObtainPairView,   TokenRefreshView )

from django.urls import path

urlpatterns = [
    path('signin', Signin.as_view()),
    path('signup', Signup.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user', GetUser.as_view()),
    path('logout', Logout.as_view(), name='logout'),
    path('groups/', GroupListCreateView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', GroupRetrieveUpdateDestroyView.as_view(), name='group-retrieve-update-destroy'),
    path('groups/<int:pk>/users/', GroupUsersView.as_view(), name='group-users'),
    path('permissions/', PermissionListView.as_view(), name='permission-list'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserRetrieveUpdateView.as_view(), name='user-retrieve-update'),
]