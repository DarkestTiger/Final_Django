from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from accounts.models import User
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from articles.models import Article, Comment, Saved
from articles.serializers import ArticleSerializer, CommentSerializer, ArticleSavedSerializer



#회원가입 기능
class UserSignUp(APIView):
    def post(self,request):
        data=request.data        
        username = data.get("username")
        email = data.get("email")
        errors = {}
        if not email or not username:
            errors["error"] = "email or username is required"
        else:
            if get_user_model().objects.filter(email=email).exists():
                errors["email"] = "이미 존재하는 email 입니다."
            if get_user_model().objects.filter(username=username).exists():
                errors["username"] = "이미 존재하는 username 입니다. "
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=data.get("password"),
            introduce = data.get("introduce"),
            address = data.get("address")
        )
        return Response({
            "id":user.id,
            "username":user.username,
            "email":user.email,
            "introduce":user.introduce,
            "address":user.address
        },
        status=status.HTTP_201_CREATED)

# 로그인 기능
class UserLogIn(APIView):
    def post(self,request):
        username = request.data["username"]
        password = request.data["password"]
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({"message":"존재하지 않는 아이디입니다."},status=status.HTTP_400_BAD_REQUEST)
        if not check_password(password,user.password):
            return Response({"message":"비밀번호가 틀립니다."},status=status.HTTP_400_BAD_REQUEST)
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response=Response(
                {
                    'user' : UserSerializer(user).data,
                    "jwt_token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token
                    },
                },
            status=status.HTTP_200_OK)
            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        else:
            return Response({"message":"로그인 실패입니다."},status=status.HTTP_400_BAD_REQUEST)

# 로그아웃 기능
class UserLogOut(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        response = Response({"detail":"로그아웃 완료"},status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                response.delete_cookie('refresh_token')
            except Exception as e:
                response = Response({"message":"로그아웃에 실패했습니다."},status=status.HTTP_400_BAD_REQUEST)
            return response
        return Response({"message":"로그인을 해주세요"},status=status.HTTP_400_BAD_REQUEST)

# 프로필 수정 기능
class UpdateUserDetails(APIView):
    pass

# 회원 탈퇴기능
class DeleteProfile(APIView):
    pass

# 보여지는 프로필 페이지
@api_view(['GET'])
def user_profile(request, username):

    user = get_object_or_404(User,username = username)
    user_articles = Article.objects.filter(author = user)
    user_comment = Comment.objects.filter(author = user)
    like_articles = Article.objects.filter(like_users = user)
    like_comment = Comment.objects.filter(like_users = user)
    saved_list = Saved.objects.filter(owner = user)

    following = user.following.all()
    following_user = [u.username for u in following]

    serializer = UserProfileSerializer(user)
    article_serializer = ArticleSerializer(user_articles, many = True )
    comment_serializer = CommentSerializer(user_comment, many = True )
    like_article_serializer = ArticleSerializer(like_articles, many = True)
    like_comment_serializer = CommentSerializer(like_comment, many = True)
    saved_list_serializer = ArticleSavedSerializer(saved_list, many=True)

    response_data = {
        'user': serializer.data,

        'following': following_user,

        'written_articles' : article_serializer.data,
        'written_comment' : comment_serializer.data,

        'like_articles' : like_article_serializer.data,
        'like_comment' : like_comment_serializer.data,

        'saved_list' : saved_list_serializer.data,
    }

    return Response(response_data)

# 팔로우
class UserFollow(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, username):
        user = get_object_or_404(User, username = username)
        if request.user == user:
            return Response({"error":"자기 자신을 팔로우 할 수 없습니다." }, status = status.HTTP_400_BAD_REQUEST)
        if request.user in user.follower.all():
            return Response({"error":"이미 팔로우를 했습니다." }, status = status.HTTP_400_BAD_REQUEST)
        user.follower.add(request.user)
        return Response({"success":"팔로우 완료" }, status = status.HTTP_201_CREATED)

# 언팔로우
    @permission_classes([IsAuthenticated])
    def delete(self, request, username):
        user = get_object_or_404(User,username = username)
        if request.user == user:
            return Response({"error":"자기 자신을 언팔로우 할 수 없습니다." }, status = status.HTTP_400_BAD_REQUEST)
        if request.user not in user.follower.all():
            return Response({"error":"팔로우 한 적이 없습니다." }, status = status.HTTP_400_BAD_REQUEST)
        user.follower.remove(request.user)
        return Response({"success":"언팔로우 완료" }, status = status.HTTP_204_NO_CONTENT)
    


