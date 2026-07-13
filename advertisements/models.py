from django.db import models
from django.utils import timezone
class Advertisement(models.Model):
    PLACEMENTS = (("home_sidebar", "Homepage sidebar"), ("home_wide", "Homepage wide"), ("article_sidebar", "Article sidebar"), ("article_inline", "Article inline"))
    STYLES = (("creative", "Text creative"), ("image", "Image banner"))
    name = models.CharField("Internal name", max_length=120)
    advertiser = models.CharField("Advertiser label", max_length=120, blank=True)
    headline = models.CharField(max_length=180, blank=True)
    subheadline = models.CharField(max_length=220, blank=True)
    contact = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to="advertisements/%Y/%m/", blank=True, null=True)
    destination_url = models.URLField(blank=True)
    cta_text = models.CharField(max_length=40, default="Call Now", blank=True)
    placement = models.CharField(max_length=30, choices=PLACEMENTS, default="home_sidebar")
    style = models.CharField(max_length=12, choices=STYLES, default="creative")
    priority = models.PositiveSmallIntegerField(default=0)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ("-priority", "-created_at")
    def __str__(self): return self.name
    @property
    def is_current(self):
        now = timezone.now()
        return self.is_active and (not self.starts_at or self.starts_at <= now) and (not self.ends_at or self.ends_at >= now)
    @property
    def action_url(self):
        if self.destination_url: return self.destination_url
        if self.whatsapp:
            number = "".join(filter(str.isdigit, self.whatsapp))
            return f"https://wa.me/{'91' + number if len(number) == 10 else number}"
        if self.contact: return f"tel:{''.join(ch for ch in self.contact if ch.isdigit() or ch == '+')}"
        return ""
