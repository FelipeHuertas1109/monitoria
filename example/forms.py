# app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        help_text="Ingrese su dirección de correo electrónico."
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmación de contraseña',
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_.',
            'password1': (
                'Tu contraseña no puede ser demasiado similar a tu otra información personal.\n'
                'Tu contraseña debe contener al menos 8 caracteres.\n'
                'Tu contraseña no puede ser una contraseña común.\n'
                'Tu contraseña no puede ser completamente numérica.'
            ),
            'password2': 'Introduce la misma contraseña que antes, para verificación.'
        }

class BaseDayPreferenceForm(forms.ModelForm):
    """
    Formulario base para las preferencias diarias (campos comunes: morning, afternoon y cont).
    """
    class Meta:
        fields = ['morning', 'afternoon']

class MondayForm(BaseDayPreferenceForm):
    class Meta(BaseDayPreferenceForm.Meta):
        model = Monday

class TuesdayForm(BaseDayPreferenceForm):
    class Meta(BaseDayPreferenceForm.Meta):
        model = Tuesday

class WednesdayForm(BaseDayPreferenceForm):
    class Meta(BaseDayPreferenceForm.Meta):
        model = Wednesday

class ThursdayForm(BaseDayPreferenceForm):
    class Meta(BaseDayPreferenceForm.Meta):
        model = Thursday

class FridayForm(BaseDayPreferenceForm):
    class Meta(BaseDayPreferenceForm.Meta):
        model = Friday

class SaturdayForm(BaseDayPreferenceForm):
    class Meta(BaseDayPreferenceForm.Meta):
        model = Saturday

class SundayForm(BaseDayPreferenceForm):
    class Meta(BaseDayPreferenceForm.Meta):
        model = Sunday
