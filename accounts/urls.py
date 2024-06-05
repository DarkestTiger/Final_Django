from django.urls import path

from accounts import views, templates_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'


templates_urlpatterns = [
    path("signup/", templates_views.signup, name='signup'),
    path("login/", templates_views.login, name='login'),
    path("profile/", templates_views.profile, name='profile'),
    path("profile/modify/", templates_views.modify, name='modify'),
]

drf_urlpatterns = [ path("auth/signup/", views.UserSignUp.as_view(), name='api_signup'),
    path("auth/login/", views.UserLogIn.as_view(), name='api_logout'),
    path("auth/logout/", views.UserLogOut.as_view(), name='api_logout'),
    path("auth/<str:username>/", views.user_profile, name='api_profile'),
    path("auth/<str:username>/modify", views.UpdateProfileView.as_view(), name='api_modify'),
    path("auth/<str:username>/delete/", views.DeleteProfile.as_view(), name='api_profile'),
    path("auth/<str:username>/follow/", views.UserFollow.as_view(), name='api_follow'),
]

urlpatterns = drf_urlpatterns + templates_urlpatterns

