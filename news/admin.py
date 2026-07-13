from django.contrib import admin
from .models import Article
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "city", "status", "is_breaking", "published_at")
    list_filter = ("status", "category", "is_breaking", "is_featured"); search_fields = ("title", "summary", "content"); prepopulated_fields = {"slug": ("title",)}
