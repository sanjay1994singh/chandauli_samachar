from django.db import models
from django.urls import reverse

from chandauli_samachar.fields import CompleteUnicodeSlugField
from chandauli_samachar.slugs import unique_slug


class Category(models.Model):
    name = models.CharField("Name", max_length=100, unique=True)
    slug = CompleteUnicodeSlugField(
        "Slug", unique=True, blank=True, allow_unicode=True,
        help_text="Automatically generated from the Hindi or English name.",
    )
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=30, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta: ordering = ("order", "name"); verbose_name_plural = "Categories"
    def __str__(self): return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name, fallback="category", max_length=50)
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse("category_articles", args=[self.slug])
