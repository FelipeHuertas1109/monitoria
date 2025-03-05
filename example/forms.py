# app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm

class RecoverHoursForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        label="Usuario",
        empty_label="Seleccione un usuario...",
        widget=forms.Select(attrs={
            'class': (
                'w-full border border-gray-300 rounded px-3 py-2 '
                'focus:outline-none focus:ring-2 focus:ring-blue-500 '
                'dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100'
            )
        })
    )
    period = forms.ChoiceField(
        choices=[('morning', 'Mañana'), ('afternoon', 'Tarde')],
        label="Período",
        widget=forms.Select(attrs={
            'class': (
                'w-full border border-gray-300 rounded px-3 py-2 '
                'focus:outline-none focus:ring-2 focus:ring-blue-500 '
                'dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100'
            )
        })
    )
    hours = forms.FloatField(
        label="Horas a recuperar",
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': (
                'w-full border border-gray-300 rounded px-3 py-2 '
                'focus:outline-none focus:ring-2 focus:ring-blue-500 '
                'dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100'
            )
        })
    )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }
        # Se definen vacíos para evitar los textos por defecto
        help_texts = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remover los textos de ayuda de los campos de contraseña
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        # Actualizar los labels (por si acaso)
        self.fields['username'].label = "Nombre de usuario"
        self.fields['email'].label = "Correo electrónico"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"
        

class BaseDayPreferenceForm(forms.ModelForm):
    """
    Formulario base para las preferencias diarias (campos comunes: morning, afternoon, sede_morning y sede_afternoon).
    """
    class Meta:
        fields = ['morning', 'afternoon', 'sede_morning', 'sede_afternoon']
        labels = {
            'morning': 'Mañana',
            'afternoon': 'Tarde',
            'sede_morning': 'Sede Mañana',
            'sede_afternoon': 'Sede Tarde'
        }

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
