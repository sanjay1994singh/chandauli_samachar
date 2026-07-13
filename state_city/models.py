from django.db import models
class State(models.Model):
    name = models.CharField(max_length=100, unique=True); slug = models.SlugField(unique=True)
    def __str__(self): return self.name
class City(models.Model):
    state = models.ForeignKey(State, related_name="cities", on_delete=models.CASCADE)
    name = models.CharField(max_length=100); slug = models.SlugField()
    class Meta: unique_together = ("state", "slug"); verbose_name_plural = "Cities"
    def __str__(self): return f"{self.name}, {self.state.name}"
