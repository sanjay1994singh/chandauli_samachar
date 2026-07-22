from django.contrib import admin

from chandauli_samachar.admin import UnicodeSlugAdminMixin

from .models import Article
@admin.register(Article)
class ArticleAdmin(UnicodeSlugAdminMixin, admin.ModelAdmin):
    list_display = ("title", "category", "city", "status", "is_breaking", "created_at", "published_at")
    ordering = ("-created_at", "-pk")
    readonly_fields = ("created_at", "updated_at", "views")
    list_filter = ("status", "category", "is_breaking", "is_featured"); search_fields = ("title", "summary", "content"); prepopulated_fields = {"slug": ("title",)}
