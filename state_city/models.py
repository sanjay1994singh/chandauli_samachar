from django.db import models

from chandauli_samachar.fields import CompleteUnicodeSlugField
from chandauli_samachar.slugs import unique_slug


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = CompleteUnicodeSlugField(
        unique=True, blank=True, allow_unicode=True,
        help_text="Automatically generated from the Hindi or English name.",
    )
    def __str__(self): return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name, fallback="state", max_length=50)
        super().save(*args, **kwargs)


class City(models.Model):
    state = models.ForeignKey(State, related_name="cities", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = CompleteUnicodeSlugField(
        blank=True, allow_unicode=True,
        help_text="Automatically generated from the Hindi or English name.",
    )
    class Meta: unique_together = ("state", "slug"); verbose_name_plural = "Cities"
    def __str__(self): return f"{self.name}, {self.state.name}"
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(
                self,
                self.name,
                fallback="city",
                max_length=50,
                queryset=City.objects.filter(state=self.state),
            )
        super().save(*args, **kwargs)
