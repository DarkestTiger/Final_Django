from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'

urlpatterns = [
    path("auth/signup/", views.UserSignUp.as_view(), name='signup'),
    path("auth/login/", views.UserLogIn.as_view(), name='logout'),
    path("auth/logout/", views.UserLogOut.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
