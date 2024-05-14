from django.shortcuts import render

from rest_framework.views import APIView

#회원가입 기능
class UserSignUp(APIView): # APIView 클래스의 as_view 함수를 사용.
    pass

# 로그인 기능
class UserLogIn(APIView):
    pass

# 프로필 수정 기능
class UpdateUserDetails(APIView):
    pass

# 회원 탈퇴기능
class DeleteProfile(APIView):
    pass
