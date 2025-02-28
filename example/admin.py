from django.contrib import admin
from .models import (
    Sede, Monday, Tuesday, Wednesday,
    Thursday, Friday, Saturday, Sunday
)

# 1. Registrar la tabla Sede (booleana) para edición independiente.
@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ("user", "barcelona", "san_antonio")
    list_filter = ("barcelona", "san_antonio")
    search_fields = ("user__username",)

# 2. Registrar tus modelos de días (Monday, Tuesday, etc.)
models = [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]

@admin.register(*models)
class DayPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "morning", "afternoon",
        "morning_hours", "afternoon_hours",
        "sede_morning", "sede_afternoon",
        "cont", "morning_marked", "afternoon_marked",
        "morning_authorized", "afternoon_authorized",
    )
    list_filter = (
        "morning", "afternoon",
        "morning_authorized", "afternoon_authorized",
        "sede_morning", "sede_afternoon",
    )
    search_fields = ("user__username",)
    ordering = ("user",)
