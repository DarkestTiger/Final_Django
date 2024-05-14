from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated

from .models import Article,Comment
from .serializers import ArticleSerializer,ArticleDetailSerializer,CommentSerializer

# 게시판 구현
# 게시글 목록
class ArticleListAPIView(APIView):
    # 게시글 목록 조회
    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data)

    # 게시글 생성
    # @permission_classes([IsAuthenticated])
    def post(self, request):
        content = request.data.get("content")
        if not content:
            return Response({"error": "content is required"}, status=400)

        article = Article.objects.create(
            content=content,
        )
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
    # @permission_classes([IsAuthenticated])
    def put(self, request, articleId):
        # user = request.user
        article = self.get_object(articleId)
        # if user == article.user:
        #     serializer = ArticleDetailSerializer(
        #         article, data=request.data, partial=True
        #     )

        #     if serializer.is_valid(raise_exception=True):
        #         serializer.save()
        #         return Response(serializer.data)
        # return Response({"error": "You are not the author of this article"}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleDetailSerializer(
                article, data=request.data, partial=True
            )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    # 게시글 삭제
    # @permission_classes([IsAuthenticated])
    def delete(self, request, articleId):
        # user = request.user
        article = self.get_object(articleId)

        # if user == article.user:
        #     article.delete()
        #     data = {"pk": f"{articleId} is deleted."}
        #     return Response(data, status=status.HTTP_200_OK)
        # return Response({"error": "You are not the author of this article"}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        data = {"pk": f"{articleId} is deleted."}
        return Response(data, status=status.HTTP_200_OK)
    
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
    # @permission_classes([IsAuthenticated])
    def post(self, request, articleId):
        article = self.get_article(articleId)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.validated_data.get('comment')
            if not comment.strip():
                raise ValidationError("Comment cannot be empty")
            
            # serializer.save(user=request.user, article=article)
            serializer.save(article=article)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
    # @permission_classes([IsAuthenticated])
    def put(self, request, commentId):
        comment = self.get_comment(commentId)
        # if comment.user != request.user:
        #     return Response({"error": "You are not the author of this comment"}, status=status.HTTP_403_FORBIDDEN)

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
    # @permission_classes([IsAuthenticated])
    def delete(self, request, commentId):
        comment = self.get_comment(commentId)

        # if comment.user != request.user:
        #     return Response({"error": "You are not the author of this comment"}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()

        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)