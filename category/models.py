from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField("Name", max_length=100, unique=True)
    slug = models.SlugField(
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
            base = slugify(self.name, allow_unicode=True)[:40] or "category"
            candidate, counter = base, 2
            while Category.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                suffix = f"-{counter}"
                candidate = f"{base[:50 - len(suffix)]}{suffix}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse("category_articles", args=[self.slug])
