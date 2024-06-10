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
    path("profile/modify/", templates_views.modify, name='modify'),
    path('profile/<str:username>/', views.user_profile, name='user-profile'),
]

drf_urlpatterns = [ 
    path("auth/signup/", views.UserSignUp.as_view(), name='api_signup'),
    path("auth/login/", views.UserLogIn.as_view(), name='api_login'),
    path("auth/logout/", views.UserLogOut.as_view(), name='api_logout'),
    path("auth/recommend/", views.profile_recommend, name='profile_recommend'), # 아래에 두면 username때문에 걸림.
    path("auth/<str:username>/", views.api_user_profile, name='api_profile'),
    path("auth/<str:username>/modify/", views.UpdateProfileView.as_view(), name='api_modify'),
    path("auth/<str:username>/delete/", views.DeleteProfile.as_view(), name='api_profile'),
    # path("auth/<str:username>/follow/", views.UserFollow.as_view(), name='api_follow'),
    path('map/', views.map_view, name='map_view'), # 구글 지도 view
    path('profile/<str:username>/follow/', views.follow_unfollow_user, name='follow-unfollow-user'),
]

urlpatterns = templates_urlpatterns + drf_urlpatterns


