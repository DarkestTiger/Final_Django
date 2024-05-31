from django.urls import path

from accounts import views
from django.urls import path # 구글 위치 API
from . import views # 구글 위치 API

app_name = 'accounts'

urlpatterns = [
    path("auth/signup/", views.UserSignUp.as_view(), name='signup'),
    path("auth/login/", views.UserLogIn.as_view(), name='logout'),
    path("auth/logout/", views.UserLogOut.as_view(), name='logout'),
    path("auth/<str:username>/", views.user_profile, name='profile'),
    path("auth/<str:username>/follow/", views.UserFollow.as_view(), name='follow'),
    path('get-location/', views.get_location_data, name='get_location_data'), # 구글 위치 API
    path('map/', views.map_view, name='map_view') # 구글 지도 view
]