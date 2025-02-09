from django.db import models
from django.contrib.auth.models import User

class Monday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="monday")
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    cont = models.IntegerField(default=0)

    def __str__(self):
        return f"Preferencias de {self.user.username} - Lunes"

class Tuesday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tuesday")
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    cont = models.IntegerField(default=0)

    def __str__(self):
        return f"Preferencias de {self.user.username} - Martes"

class Wednesday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wednesday")
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    cont = models.IntegerField(default=0)

    def __str__(self):
        return f"Preferencias de {self.user.username} - Miércoles"

class Thursday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="thursday")
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    cont = models.IntegerField(default=0)

    def __str__(self):
        return f"Preferencias de {self.user.username} - Jueves"

class Friday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="friday")
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    cont = models.IntegerField(default=0)

    def __str__(self):
        return f"Preferencias de {self.user.username} - Viernes"

class Saturday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="saturday")
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    cont = models.IntegerField(default=0)

    def __str__(self):
        return f"Preferencias de {self.user.username} - Sábado"

class Sunday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="sunday")
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    cont = models.IntegerField(default=0)

    def __str__(self):
        return f"Preferencias de {self.user.username} - Domingo"
