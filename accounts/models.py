from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    phone = models.CharField("मोबाइल", max_length=15, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    bio = models.TextField("परिचय", blank=True)
    is_reporter = models.BooleanField("रिपोर्टर", default=False)
    city = models.ForeignKey("state_city.City", on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self): return self.get_full_name() or self.username
