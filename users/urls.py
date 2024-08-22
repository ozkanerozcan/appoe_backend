from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.UserRegisterationAPIView.as_view(), name="create-user"),
    path("login/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout-user"),
    path("me/", views.UserAPIView.as_view(), name="user-info"),
    path("user/edit/", views.UserEditAPIView.as_view(), name="user-edit"),
    path('activate/', views.ActivateEmail, name='activate-email'),
    path('user/list/', views.UserListView.as_view(), name='user-list'),
    path('user/change-password/', views.ChangePasswordView.as_view(), name='user-change-password'),
    path('user/change-avatar/', views.UserAvatarAPIView.as_view(), name='user-change-avatar'),
]
