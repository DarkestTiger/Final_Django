from django.urls import path
from articles import views, template_views
from accounts.views import user_profile, follow_unfollow_user  # accounts의 user_profile 뷰를 가져옴

app_name = 'articles'

template_urlpatterns = [
    path("list/template/", template_views.article_list_template_view, name="list-template"),
    path("create/template/", template_views.article_create_template_view, name="create-template"),
    path("<int:articleId>/template/",template_views.article_detail_template_view, name="detail-template"),
    path("<int:articleId>/update/template/", template_views.article_update_template_view, name="update-template"),
    path("comment/<int:commentId>/template/", template_views.comment_detail_view, name="comment-detail-template"),
    path("saved/template/",template_views.saved_list_template_view, name="saved-list-template"),
    path("saved/create/template/",template_views.saved_create_template_view, name="saved-create-template"),
    path("saved/<int:savedId>/template/", template_views.saved_detail_template_view, name="saved-detail-template"),
    path("saved/<int:savedId>/update/template/", template_views.saved_update_template_view, name="saved-update-template"),
    path("search/<str:hashtag>/template/", template_views.hashtag_search_template_view, name="hashtag-search-template"),
    path("routinegpt/template/", template_views.routine_gpt_template_view, name="routine-gpt-template"),
    path("dietgpt/template/", template_views.diet_gpt_template_view, name="diet-gpt-template")
]

drf_urlpatterns = [
    # article list
    path("", views.ArticleListAPIView.as_view(), name='article_list'),

    # article detail
    path("<int:articleId>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    path("<int:articleId>/comment/", views.CommentListAPIView.as_view(), name="comment_list"),
    path("<int:articleId>/like/", views.ArticleLikeAPIView.as_view(), name="article_like"),

    # comment
    path("comment/<int:commentId>/", views.CommentDetailAPIView.as_view(), name="comment_detail"),
    path("comment/<int:commentId>/like/", views.CommentLikeAPIView.as_view(), name="comment_like"),

    # hashtag search
    path("search/<str:hashtag>/", views.hashtag_search, name="hashtag_search"),

    # saved articles
    path("saved/", views.SavedListAPIView.as_view(), name="saved_list"),
    path("saved/<int:savedId>/", views.SavedDetailAPIView.as_view(), name="saved_detail"),
    path("saved/<int:savedId>/<int:articleId>/", views.ArticleSavedAPIView.as_view(), name="article_saved"),

    # chat-gpt
    path("routinegpt/", views.routine_gpt, name="routine_gpt"),
    path("dietgpt/", views.diet_gpt, name="diet_gpt"),
    
    # view profile
    path('profile/<str:username>/', user_profile, name='profile-redirect'),
    path('profile/<str:username>/follow/', follow_unfollow_user, name='follow-unfollow-user'),

]

urlpatterns = drf_urlpatterns + template_urlpatterns
