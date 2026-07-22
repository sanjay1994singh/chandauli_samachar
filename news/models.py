from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Article(models.Model):
    STATUS = (("draft", "Draft"), ("published", "Published"))
    title = models.CharField("Title", max_length=250)
    slug = models.SlugField(
        "Slug",
        max_length=270,
        unique=True,
        blank=True,
        allow_unicode=True,
        help_text="Automatically generated from the Hindi or English title.",
    )
    summary = models.TextField(
        "Summary",
        max_length=500,
        blank=True,
        help_text="Optional: add a short summary or leave it blank.",
    )
    content = models.TextField("Content")
    featured_image = models.ImageField(upload_to="articles/%Y/%m/", blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="Demo/external image URL")
    category = models.ForeignKey("category.Category", related_name="articles", on_delete=models.PROTECT)
    state = models.ForeignKey("state_city.State", on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey("state_city.City", on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS, default="draft")
    is_breaking = models.BooleanField(default=False); is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True); created_at = models.DateTimeField(auto_now_add=True); updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ("-published_at", "-created_at")
    def __str__(self): return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title, allow_unicode=True)[:250] or "article"
            candidate, counter = base, 2
            while Article.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                suffix = f"-{counter}"
                candidate = f"{base[:270 - len(suffix)]}{suffix}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse("article_detail", args=[self.slug])
    @property
    def display_image(self): return self.featured_image.url if self.featured_image else self.image_url
