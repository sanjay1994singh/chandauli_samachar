from django.db import models
from django.utils.text import slugify


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(
        unique=True, blank=True, allow_unicode=True,
        help_text="Automatically generated from the Hindi or English name.",
    )
    def __str__(self): return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=True)[:40] or "state"
            candidate, counter = base, 2
            while State.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                suffix = f"-{counter}"
                candidate = f"{base[:50 - len(suffix)]}{suffix}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)


class City(models.Model):
    state = models.ForeignKey(State, related_name="cities", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        blank=True, allow_unicode=True,
        help_text="Automatically generated from the Hindi or English name.",
    )
    class Meta: unique_together = ("state", "slug"); verbose_name_plural = "Cities"
    def __str__(self): return f"{self.name}, {self.state.name}"
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=True)[:40] or "city"
            candidate, counter = base, 2
            queryset = City.objects.exclude(pk=self.pk).filter(state=self.state)
            while queryset.filter(slug=candidate).exists():
                suffix = f"-{counter}"
                candidate = f"{base[:50 - len(suffix)]}{suffix}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)
