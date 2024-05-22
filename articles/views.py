from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from .models import Article,Comment,Hashtag,Saved
from .serializers import ArticleSerializer,ArticleDetailSerializer,CommentSerializer,ArticleSavedSerializer


# 게시판 구현
# 게시글 목록
class ArticleListAPIView(APIView):
    # 게시글 목록 조회
    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data)

    # 게시글 생성
    @permission_classes([IsAuthenticated])
    def post(self, request):
        content = request.data.get("content")
        # ','로 해시태그 구분 가능 ex) hashtags = "안녕,반가워"
        hashtags = request.data.get("hashtags", [])
        image = request.data.get("image")
        if not content:
            return Response({"error": "content is required"}, status=400)

        article = Article.objects.create(author=request.user, content=content, image=image)

        for name in hashtags.split(','):
            hashtag, _ = Hashtag.objects.get_or_create(name=name)
            article.hashtags.add(hashtag)

        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 게시글 디테일
class ArticleDetailAPIView(APIView):
    def get_object(self, articleId):
        return get_object_or_404(Article, pk=articleId)

    # 게시글 디테일 조회
    def get(self, request, articleId):
        article = self.get_object(articleId)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)
    
    # 게시글 수정
    @permission_classes([IsAuthenticated])
    def put(self, request, articleId):
        user = request.user
        article = self.get_object(articleId)
        if user != article.author:
            return Response({"error": "You are not the author of this article"}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get("content", None)
        # ','로 해시태그 구분 가능 ex) hashtags = "안녕,반가워"
        hashtags = request.data.get("hashtags", None)
        image = request.data.get("image", None)

        if content is not None:
            article.content = content

        if hashtags is not None:
            article.hashtags.clear()
            for name in hashtags.split(','):
                hashtag, _ = Hashtag.objects.get_or_create(name=name)
                article.hashtags.add(hashtag)

        if image is not None:
            article.image = image

        article.save()
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    # 게시글 삭제
    @permission_classes([IsAuthenticated])
    def delete(self, request, articleId):
        user = request.user
        article = self.get_object(articleId)

        if user == article.author:
            article.delete()
            data = {"pk": f"{articleId} is deleted."}
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": "You are not the author of this article"}, status=status.HTTP_403_FORBIDDEN)
        # article.delete()
        # data = {"pk": f"{articleId} is deleted."}
        # return Response(data, status=status.HTTP_200_OK)
    
# 댓글 목록
class CommentListAPIView(APIView):
    def get_article(self, articleId):
        return get_object_or_404(Article, pk=articleId)
    
    # 해당 게시글의 댓글 목록 조회
    def get(self, request, articleId):
        article = self.get_article(articleId)
        comments = Comment.objects.filter(article=article)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    # 해당 게시글에 댓글 작성
    @permission_classes([IsAuthenticated])
    def post(self, request, articleId):
        article = self.get_article(articleId)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.validated_data.get('comment')
            if not comment.strip():
                raise ValidationError("Comment cannot be empty")
            
            serializer.save(author=request.user, article=article)
            # serializer.save(article=article)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 좋아요
class ArticleLikeAPIView(APIView):
    def get(self, request, articleId):
        article = get_object_or_404(Article, pk=articleId)
        like_users = article.like_users.all()
        usernames = [user.username for user in like_users]
        return Response({"like_users": usernames})
    
    # 게시글 좋아요
    @permission_classes([IsAuthenticated])
    def post(self, request, articleId):
        article = get_object_or_404(Article, pk=articleId)
        user = request.user

        if user in article.like_users.all():
            return Response({"error": "You have already liked this article."}, status=status.HTTP_400_BAD_REQUEST)

        article.like_users.add(user)
        return Response({"success": "You like the article."}, status=status.HTTP_201_CREATED)
    
    # 게시글 좋아요 삭제
    @permission_classes([IsAuthenticated])
    def delete(self, request, articleId):
        article = get_object_or_404(Article, pk=articleId)
        user = request.user

        if user not in article.like_users.all():
            return Response({"error": "You have not liked this article."}, status=status.HTTP_400_BAD_REQUEST)

        article.like_users.remove(user)
        return Response({"success": "You unliked the article."}, status=status.HTTP_204_NO_CONTENT)

# 댓글 디테일
class CommentDetailAPIView(APIView):
    def get_comment(self, commentId):
        return get_object_or_404(Comment, pk=commentId)
    
    # 댓글 디테일 조회
    def get(self, request, commentId):
        comment = self.get_comment(commentId)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    # 댓글 수정
    @permission_classes([IsAuthenticated])
    def put(self, request, commentId):
        comment = self.get_comment(commentId)
        if comment.author != request.user:
            return Response({"error": "You are not the author of this comment"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(
            comment, data=request.data, partial=True)

        if serializer.is_valid():
            content = serializer.validated_data.get('comment')
            if not content.strip():
                raise ValidationError("Comment cannot be empty")
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 댓글 삭제
    @permission_classes([IsAuthenticated])
    def delete(self, request, commentId):
        comment = self.get_comment(commentId)

        if comment.author != request.user:
            return Response({"error": "You are not the author of this comment"}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()

        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# 댓글 좋아요
class CommentLikeAPIView(APIView):
    def get(self, request, commentId):
        comment = get_object_or_404(Comment, pk=commentId)
        like_users = comment.like_users.all()
        usernames = [user.username for user in like_users]
        return Response({"like_users": usernames})
    
    # 댓글 좋아요
    @permission_classes([IsAuthenticated])
    def post(self, request, commentId):
        comment = get_object_or_404(Comment, pk=commentId)
        user = request.user

        # 이미 좋아요를 누른 유저는 에러 발생
        if user in comment.like_users.all():
            return Response({"error": "You have already liked this comment."}, status=status.HTTP_400_BAD_REQUEST)

        comment.like_users.add(user)

        return Response({"success": "You liked the comment."}, status=status.HTTP_201_CREATED)

    # 댓글 좋아요 삭제
    @permission_classes([IsAuthenticated])
    def delete(self, request, commentId):
        comment = get_object_or_404(Comment, pk=commentId)
        user = request.user

        # 좋아요를 누르지 않은 유저는 에러 발생
        if user not in comment.like_users.all():
            return Response({"error": "You have not liked this comment."}, status=status.HTTP_400_BAD_REQUEST)

        comment.like_users.remove(user)

        return Response({"success": "You unliked the comment."}, status=status.HTTP_204_NO_CONTENT)

# 해시태그 검색
@api_view(['GET'])
def hashtag_search(request, hashtag):
    article_list=Article.objects.filter(hashtags__name=hashtag)
    serializer = ArticleSerializer(article_list, many=True)
    return Response(serializer.data)


# 저장 목록
class SavedListAPIView(APIView):
    # 저장 목록 전체 조회
    def get(self, request):
        saved = Saved.objects.all()
        serializer = ArticleSavedSerializer(saved, many=True)
        return Response(serializer.data)

    # 저장 목록 생성
    @permission_classes([IsAuthenticated])
    def post(self, request):
        name = request.data.get("name")
        
        if not name:
            return Response({"error": "name is required"}, status=400)

        saved = Saved.objects.create(owner=request.user, name=name)

        serializer = ArticleSavedSerializer(saved)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 저장 목록 조회
class SavedDetailAPIView(APIView):
    def get_object(self, savedId):
        return get_object_or_404(Saved, pk=savedId)

    # 저장 목록 내용 조회
    def get(self, request, savedId):
        saved = self.get_object(savedId)
        saved_list = saved.saved_articles.all()
        articles = [s.content for s in saved_list]
        return Response({"saved articles": articles})

    # 저장 목록 이름 수정
    @permission_classes([IsAuthenticated])
    def put(self, request, savedId):
        user = request.user
        saved = self.get_object(savedId)
        if user != saved.owner:
            return Response({"error": "You are not the owner of this saved list!"}, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get("name", None)
        hashtags = request.data.get("hashtags", None)
        image = request.data.get("image", None)

        if name is not None:
            saved.name = name

        saved.save()
        serializer = ArticleSavedSerializer(saved)
        return Response(serializer.data)

    # 저장 목록 삭제
    @permission_classes([IsAuthenticated])
    def delete(self, request, savedId):
        user = request.user
        saved = self.get_object(savedId)

        if user == saved.owner:
            saved.delete()
            return Response({"success": "saved list successfully deleted."}, status=status.HTTP_200_OK)
        return Response({"error": "You are not the owner of this saved list!"}, status=status.HTTP_403_FORBIDDEN)

# 게시글 저장됨
class ArticleSavedAPIView(APIView):
    # 해당 저장목록에 게시글 저장
    @permission_classes([IsAuthenticated])
    def post(self, request, savedId, articleId):
        saved = get_object_or_404(Saved, pk=savedId)
        article = get_object_or_404(Article, pk=articleId)
        user = request.user

        if user != saved.owner:
            return Response({"error": "You are not the owner of this saved list!"}, status=status.HTTP_403_FORBIDDEN)
        
        # 이미 저장을 한 경우 에러 발생
        if saved.saved_articles.filter(id=articleId).exists():
            return Response({"error": "You have already saved this article."}, status=status.HTTP_400_BAD_REQUEST)

        saved.saved_articles.add(article)

        return Response({"success": "You saved the article in saved list."}, status=status.HTTP_201_CREATED)
    
    # 게시글 저장 취소
    @permission_classes([IsAuthenticated])
    def delete(self, request, savedId, articleId):
        saved = get_object_or_404(Saved, pk=savedId)
        article = get_object_or_404(Article, pk=articleId)
        user = request.user

        # 저장하지 않았을 경우 에러 발생
        if not saved.saved_articles.filter(id=articleId).exists():
            return Response({"error": "You have not saved this article."}, status=status.HTTP_400_BAD_REQUEST)

        saved.saved_articles.remove(article)

        return Response({"success": "You unsaved the article."}, status=status.HTTP_204_NO_CONTENT)
