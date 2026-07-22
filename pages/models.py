from django.db import models

class ContactMessage(models.Model):
    name = models.CharField("Name", max_length=120)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Phone", max_length=20)
    subject = models.CharField("Subject", max_length=180)
    message = models.TextField("Message")
    is_resolved = models.BooleanField("Resolved", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ("-created_at",)
    def __str__(self): return f"{self.name} - {self.subject}"
