# app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class BaseDayPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    morning = models.BooleanField(default=False)         # Si tiene chamba en la mañana
    afternoon = models.BooleanField(default=False)         # Si tiene chamba en la tarde
    cont = models.FloatField(default=0)                    # Contador acumulado (Float para permitir decimales)
    morning_marked = models.BooleanField(default=False)    # Indica si ya se presionó el botón en la mañana
    afternoon_marked = models.BooleanField(default=False)  # Indica si ya se presionó el botón en la tarde
    morning_authorized = models.BooleanField(default=False)    # Indica si el superusuario autorizó la mañana
    afternoon_authorized = models.BooleanField(default=False)  # Indica si el superusuario autorizó la tarde
    
    # Campos configurables para horas (ya existentes en tu implementación)
    morning_hours = models.FloatField(default=4)
    afternoon_hours = models.FloatField(default=4)
    
    # NUEVO: Campo para la sede
    sede = models.CharField(
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

