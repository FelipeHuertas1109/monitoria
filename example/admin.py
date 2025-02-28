from django.contrib import admin
from .models import Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday

# Lista de modelos a registrar
models = [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]

@admin.register(*models)
class DayPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'morning', 'afternoon', 'cont', 'morning_marked', 'afternoon_marked', 'morning_authorized', 'afternoon_authorized')
    list_filter = ('morning', 'afternoon', 'morning_authorized', 'afternoon_authorized')
    search_fields = ('user__username',)
    ordering = ('user',)
