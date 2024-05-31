from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView

from rest_framework.decorators import api_view, permission_classes

from django.conf import settings  # 구글 위치 API
from django.http import JsonResponse  # 구글 위치 API
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import get_object_or_404, render
from django.db.models import Case, When, IntegerField

from accounts.models import User

from articles.models import Article, Comment, Saved
from articles.serializers import ArticleSerializer, CommentSerializer, ArticleSavedSerializer

from .serializers import UserSerializer, UserProfileSerializer
from .regions import REGIONS, DISTRICTS

import googlemaps  # 구글 위치 API


# 회원가입 기능
class UserSignUp(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        profile_img = data.get("profile_img")
        address = data.get("address")

        # 주소 검증
        if address:
            try:
                city = address[0:2]
                district = address[3:].rstrip()
                if not district:
                    return Response({"error": """주소는 'XX XX구/군/시' 형식이어야 합니다. 
                                    예외) 세종특별자치시의 경우 읍/면/동으로 입력. 
                                    ※다음 자치시들의 경우 구까지 입력. ex) XX XX시 XX구 
                                    수원시,성남시,안양시,부천시,안산시,고양시,용인시,청주시,천안시,전주시,포항시,창원시"""},
                                    status=status.HTTP_403_FORBIDDEN)
            except ValueError:
                return Response({"error": """주소는 'XX XX구/군/시' 형식이어야 합니다. 
                                    예외) 세종특별자치시의 경우 읍/면/동으로 입력. 
                                    ※다음 자치시들의 경우 구까지 입력. ex) XX XX시 XX구 
                                    수원시,성남시,안양시,부천시,안산시,고양시,용인시,청주시,천안시,전주시,포항시,창원시"""},
                                status=status.HTTP_403_FORBIDDEN)

            index_of_city = None
            for index, (english, korean) in enumerate(REGIONS):
                if korean == city:
                    index_of_city = index
                    break

            city_eng = REGIONS[index_of_city][0]
            regions = [region for region, _ in REGIONS]

            if city_eng not in regions:
                return Response({"error": f"""주소는 'XX XX구/군/시' 형식이어야 합니다. 
                                    예외) 세종특별자치시의 경우 읍/면/동으로 입력. 
                                    ※다음 자치시들의 경우 구까지 입력. ex) XX XX시 XX구 
                                    수원시,성남시,안양시,부천시,안산시,고양시,용인시,청주시,천안시,전주시,포항시,창원시"""},
                                status=status.HTTP_403_FORBIDDEN)
            if city_eng in DISTRICTS and district not in DISTRICTS[city_eng]:
                return Response({"error": f"""주소는 'XX XX구/군/시' 형식이어야 합니다. 
                                    예외) 세종특별자치시의 경우 읍/면/동으로 입력. 
                                    ※다음 자치시들의 경우 구까지 입력. ex) XX XX시 XX구 
                                    수원시,성남시,안양시,부천시,안산시,고양시,용인시,청주시,천안시,전주시,포항시,창원시"""},
                                status=status.HTTP_403_FORBIDDEN)

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
            introduce=data.get("introduce"),
            address=address,
            profile_img=profile_img
        )

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "introduce": user.introduce,
            "address": user.address,
            "profile_image": user.get_profile_url(),
        },
            status=status.HTTP_201_CREATED)


# 로그인 기능
class UserLogIn(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({"message": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST)
        if not check_password(password, user.password):
            return Response({"message": "비밀번호가 틀립니다."}, status=status.HTTP_400_BAD_REQUEST)
        if user is not None:
            login(request, user)
            return Response({"message": "로그인 성공입니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "로그인 실패입니다."}, status=status.HTTP_400_BAD_REQUEST)


# 로그아웃 기능
class UserLogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "로그아웃 완료"}, status=status.HTTP_200_OK)


# 프로필 수정 기능
class UpdateProfileView(RetrieveUpdateAPIView):
    @permission_classes([IsAuthenticated])
    def put(self, request, username):
        data = request.data
        address = data.get("address")
        if address:
            try:
                city = address[0:2]
                district = address[3:].rstrip()
                if not district:
                    return Response({"error": """주소는 'XX XX구/군/시' 형식이어야 합니다. 
                                    예외) 세종특별자치시의 경우 읍/면/동으로 입력. 
                                    ※다음 자치시들의 경우 구까지 입력. ex) XX XX시 XX구 
                                    수원시,성남시,안양시,부천시,안산시,고양시,용인시,청주시,천안시,전주시,포항시,창원시"""},
                                    status=status.HTTP_403_FORBIDDEN)
            except ValueError:
                return Response({"error": """주소는 'XX XX구/군/시' 형식이어야 합니다. 
                                    예외) 세종특별자치시의 경우 읍/면/동으로 입력. 
                                    ※다음 자치시들의 경우 구까지 입력. ex) XX XX시 XX구 
                                    수원시,성남시,안양시,부천시,안산시,고양시,용인시,청주시,천안시,전주시,포항시,창원시"""},
                                status=status.HTTP_403_FORBIDDEN)

            index_of_city = None
            for index, (english, korean) in enumerate(REGIONS):
                if korean == city:
                    index_of_city = index
                    break

            if index_of_city is None:
                return Response({"error": "유효하지 않은 시/도입니다."}, status=status.HTTP_403_FORBIDDEN)

            city_eng = REGIONS[index_of_city][0]
            regions = [region for region, _ in REGIONS]

            if city_eng not in regions:
                return Response({"error": """주소는 'XX XX구/군/시' 형식이어야 합니다. 
                                    예외) 세종특별자치시의 경우 읍/면/동으로 입력. 
                                    ※다음 자치시들의 경우 구까지 입력. ex) XX XX시 XX구 
                                    수원시,성남시,안양시,부천시,안산시,고양시,용인시,청주시,천안시,전주시,포항시,창원시"""},
                                status=status.HTTP_403_FORBIDDEN)

            if city_eng in DISTRICTS and district not in DISTRICTS[city_eng]:
                return Response({"error": """주소는 'XX XX구/군/시' 형식이어야 합니다. 
                                    예외) 세종특별자치시의 경우 읍/면/동으로 입력. 
                                    ※다음 자치시들의 경우 구까지 입력. ex) XX XX시 XX구 
                                    수원시,성남시,안양시,부천시,안산시,고양시,용인시,청주시,천안시,전주시,포항시,창원시"""},
                                status=status.HTTP_403_FORBIDDEN)
        serializer = UserProfileSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 회원 탈퇴기능
class DeleteProfile(RetrieveDestroyAPIView):
    @permission_classes([IsAuthenticated])
    def delete(self, request, username):
        print(request)
        user = get_object_or_404(get_user_model(), username=username)
        if request.user != user:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            password = request.data.get("password")
            if not password:
                return Response({"error": "비밀번호는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

            if not request.user.check_password(password):
                return Response({"error": "비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

            request.user.delete()
            return Response({"message": "회원탈퇴완료"}, status=status.HTTP_204_NO_CONTENT)


# 보여지는 프로필 페이지
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_articles = Article.objects.filter(author=user).order_by('-created_at')
    user_comment = Comment.objects.filter(author=user)
    like_articles = Article.objects.filter(like_users=user)
    like_comment = Comment.objects.filter(like_users=user)
    saved_list = Saved.objects.filter(owner=user)

    following = user.follower.all()

    following_user = [u.username for u in following]

    serializer = UserProfileSerializer(user)
    article_serializer = ArticleSerializer(user_articles, many=True)
    comment_serializer = CommentSerializer(user_comment, many=True)
    like_article_serializer = ArticleSerializer(like_articles, many=True)
    like_comment_serializer = CommentSerializer(like_comment, many=True)
    saved_list_serializer = ArticleSavedSerializer(saved_list, many=True)

    response_data = {
        'user': serializer.data,

        'following': following_user,

        'written_articles': article_serializer.data,
        'written_comment': comment_serializer.data,

        'like_articles': like_article_serializer.data,
        'like_comment': like_comment_serializer.data,

        'saved_list': saved_list_serializer.data,
    }

    return Response(response_data)


# 팔로우
class UserFollow(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user == user:
            return Response({"error": "자기 자신을 팔로우 할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user in user.follower.all():
            return Response({"error": "이미 팔로우를 했습니다."}, status=status.HTTP_400_BAD_REQUEST)
        user.follower.add(request.user)
        return Response({"success": "팔로우 완료"}, status=status.HTTP_201_CREATED)

    # 언팔로우
    @permission_classes([IsAuthenticated])
    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user == user:
            return Response({"error": "자기 자신을 언팔로우 할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user not in user.follower.all():
            return Response({"error": "팔로우 한 적이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        user.follower.remove(request.user)
        return Response({"success": "언팔로우 완료"}, status=status.HTTP_204_NO_CONTENT)


# 프로필 추천
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_recommend(request):
    user = request.user
    user_region = user.address[0:2]
    user_district = user.address[3:].rstrip()
    users = User.objects.annotate(
        priority=Case(
            When(address__startswith=f"{user_region} {user_district}", then=1),  # 같은 지역, 같은 구
            When(address__startswith=user_region, then=2),  # 같은 지역
            default=3,  # 나머지
            output_field=IntegerField(),
        )
    ).filter(priority__lte=2).exclude(id=user.id).order_by('priority')[:5]
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# 구글 위치 API

def get_location_data(request):
    address = request.GET.get('address')
    if not address:
        return JsonResponse({'error': 'Address parameter is required'}, status=400)

    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(address)

    if not geocode_result:
        return JsonResponse({'error': 'No results found'}, status=404)

    location = geocode_result[0]['geometry']['location']
    return JsonResponse(location)


def map_view(request):
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'map_views.html', context)
