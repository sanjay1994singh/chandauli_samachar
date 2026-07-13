from django.db import models
from django.urls import reverse
class Category(models.Model):
    name = models.CharField("श्रेणी", max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=30, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta: ordering = ("order", "name"); verbose_name_plural = "Categories"
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse("category_articles", args=[self.slug])
