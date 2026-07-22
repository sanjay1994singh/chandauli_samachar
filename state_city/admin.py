from django.contrib import admin

from chandauli_samachar.admin import UnicodeSlugAdminMixin

from .models import State, City
@admin.register(State)
class StateAdmin(UnicodeSlugAdminMixin, admin.ModelAdmin): prepopulated_fields = {"slug": ("name",)}
@admin.register(City)
class CityAdmin(UnicodeSlugAdminMixin, admin.ModelAdmin): list_display = ("name", "state"); list_filter = ("state",); prepopulated_fields = {"slug": ("name",)}
