from users.views.signin import Signin
from users.views.signup import Signup
from users.views.two_factor import TwoFactorVerify
from users.views.password_reset import PasswordResetConfirm, PasswordResetRequest
from users.views.user import GetUser
from users.views.logout import Logout
from users.views.group import GroupListCreateView, GroupRetrieveUpdateDestroyView
from users.views.group_users import GroupUsersView
from users.views.permission import PermissionListView
from users.views.user_config import UserListView, UserRetrieveUpdateView
from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path

urlpatterns = [
    path('signin', Signin.as_view(), name='signin'),
    path('signup', Signup.as_view()),
    path('2fa/verify', TwoFactorVerify.as_view(), name='two_factor_verify'),
    path(
        'password-reset/request',
        PasswordResetRequest.as_view(),
        name='password_reset_request',
    ),
    path(
        'password-reset/confirm',
        PasswordResetConfirm.as_view(),
        name='password_reset_confirm',
    ),
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