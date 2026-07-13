from django.contrib import admin
from .models import State, City
@admin.register(State)
class StateAdmin(admin.ModelAdmin): prepopulated_fields = {"slug": ("name",)}
@admin.register(City)
class CityAdmin(admin.ModelAdmin): list_display = ("name", "state"); list_filter = ("state",); prepopulated_fields = {"slug": ("name",)}
