from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path("signup/", views.UserSignUp.as_view(), name='signup') # 슬래시 삭제
]