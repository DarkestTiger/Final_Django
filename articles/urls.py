from django.urls import path
from articles import views

app_name = 'articles'

urlpatterns = [
    # article list
    path("", views.ArticleListAPIView.as_view(),name='article_list'),

    # article detail
    path("<int:articleId>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    path("<int:articleId>/comment/", views.CommentListAPIView.as_view(), name="comment_list"),
    path("<int:articleId>/like/", views.ArticleLikeAPIView.as_view(), name="article_like"),

    # comment
    path("comment/<int:commentId>/", views.CommentDetailAPIView.as_view(), name="comment_detail"),
    path("comment/<int:commentId>/like/", views.CommentLikeAPIView.as_view(), name="comment_like"),
    
    # hashtag search
    path("search/<str:hashtag>/", views.hashtag_search, name="hashtag_search"),
]