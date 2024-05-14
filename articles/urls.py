from django.urls import path
from articles import views

app_name = 'articles'

urlpatterns = [
    # article list
    path("", views.ArticleListAPIView.as_view(),name='article_list'),

    # article detail
    path("<int:articleId>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    path("<int:articleId>/comment/", views.CommentListAPIView.as_view(), name="comment_list"),

    # comment
    path("comment/<int:commentId>/", views.CommentDetailAPIView.as_view(), name="comment_detail"),
    
    # hashtag search
    path("search/<str:hashtag>/", views.hashtag_search, name="hashtag_search"),
]