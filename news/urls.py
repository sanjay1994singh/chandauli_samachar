from django.urls import path
from . import views
urlpatterns = [path("", views.home, name="home"), path("search/", views.search, name="search"), path("category/<slug:slug>/", views.category_articles, name="category_articles"), path("news/<slug:slug>/", views.article_detail, name="article_detail")]
