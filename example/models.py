from django.db import models
from django.contrib.auth.models import User

class monday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)

    def __str__(self):
        return f"Preferencias de {self.user.username}"


