from django.conf import settings
from django.db import models
from django.urls import reverse
class Article(models.Model):
    STATUS = (("draft", "Draft"), ("published", "Published"))
    title = models.CharField("शीर्षक", max_length=250)
    slug = models.SlugField(max_length=270, unique=True)
    summary = models.TextField("सारांश", max_length=500)
    content = models.TextField("समाचार")
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
    def get_absolute_url(self): return reverse("article_detail", args=[self.slug])
    @property
    def display_image(self): return self.featured_image.url if self.featured_image else self.image_url
