from django.urls import path
from . import views
urlpatterns = [path("", views.home, name="home"), path("search/", views.search, name="search"), path("category/<str:slug>/", views.category_articles, name="category_articles"), path("news/<str:slug>/", views.article_detail, name="article_detail")]
