from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Chandauli Samachar Administration"
admin.site.site_title = "Chandauli Samachar Admin"
admin.site.index_title = "Website Management"

urlpatterns = [path("admin/", admin.site.urls), path("accounts/", include("accounts.urls")), path("", include("pages.urls")), path("", include("news.urls"))]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
