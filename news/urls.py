from django.urls import path
from . import views
urlpatterns = [path("", views.home, name="home"), path("search/", views.search, name="search"), path("category/<str:slug>/", views.category_articles, name="category_articles"), path("s/<int:pk>/", views.article_share, name="article_share"), path("social/article/<int:pk>.jpg", views.article_social_image, name="article_social_image"), path("news/<str:slug>/", views.article_detail, name="article_detail")]
