# accounts/models.py


from django.db import models
from django.contrib.auth.models import AbstractUser  

class CustomUser (AbstractUser ):
    email_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email  # Use email as username if not provided
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email