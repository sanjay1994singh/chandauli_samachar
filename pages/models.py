from django.db import models

class ContactMessage(models.Model):
    name = models.CharField("नाम", max_length=120)
    email = models.EmailField("ईमेल", blank=True)
    phone = models.CharField("मोबाइल", max_length=20)
    subject = models.CharField("विषय", max_length=180)
    message = models.TextField("संदेश")
    is_resolved = models.BooleanField("निस्तारित", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ("-created_at",)
    def __str__(self): return f"{self.name} - {self.subject}"
