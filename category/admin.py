from django.contrib import admin

from chandauli_samachar.admin import UnicodeSlugAdminMixin

from .models import Category
@admin.register(Category)
class CategoryAdmin(UnicodeSlugAdminMixin, admin.ModelAdmin):
    list_display = ("name", "order", "is_active"); prepopulated_fields = {"slug": ("name",)}
