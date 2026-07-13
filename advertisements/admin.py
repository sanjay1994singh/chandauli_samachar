from django.contrib import admin
from .models import Advertisement
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("name", "advertiser", "placement", "style", "priority", "is_active", "starts_at", "ends_at")
    list_filter = ("placement", "style", "is_active")
    search_fields = ("name", "advertiser", "headline", "contact", "whatsapp")
    list_editable = ("priority", "is_active")
    fieldsets = (("Creative", {"fields": ("name", "advertiser", "headline", "subheadline", "image", "style")}), ("Action", {"fields": ("contact", "whatsapp", "destination_url", "cta_text")}), ("Publishing", {"fields": ("placement", "priority", "starts_at", "ends_at", "is_active")}))
