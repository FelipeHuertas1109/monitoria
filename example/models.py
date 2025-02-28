# app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Sede(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    barcelona = models.BooleanField(default=False)
    san_antonio = models.BooleanField(default=False)

    def __str__(self):
        return f"Sede de {self.user.username}"

class BaseDayPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    morning = models.BooleanField(default=False)         # Si tiene chamba en la mañana
    afternoon = models.BooleanField(default=False)         # Si tiene chamba en la tarde
    cont = models.FloatField(default=0)
    morning_marked = models.BooleanField(default=False)
    afternoon_marked = models.BooleanField(default=False)
    morning_authorized = models.BooleanField(default=False)
    afternoon_authorized = models.BooleanField(default=False)
    
    morning_hours = models.FloatField(default=4)
    afternoon_hours = models.FloatField(default=4)
    
    # Campos de sede separados para cada período
    sede_morning = models.CharField(
        max_length=50,
        choices=[("Barcelona", "Barcelona"), ("San Antonio", "San Antonio")],
        default="Barcelona"
    )
    sede_afternoon = models.CharField(
        max_length=50,
        choices=[("Barcelona", "Barcelona"), ("San Antonio", "San Antonio")],
        default="Barcelona"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"Preferencias de {self.user.username} - {self.day_name}"


class Monday(BaseDayPreference):
    day_name = "Lunes"

class Tuesday(BaseDayPreference):
    day_name = "Martes"

class Wednesday(BaseDayPreference):
    day_name = "Miércoles"

class Thursday(BaseDayPreference):
    day_name = "Jueves"

class Friday(BaseDayPreference):
    day_name = "Viernes"

class Saturday(BaseDayPreference):
    day_name = "Sábado"

class Sunday(BaseDayPreference):
    day_name = "Domingo"

