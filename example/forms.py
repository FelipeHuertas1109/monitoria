# app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm

class RecoverHoursForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Usuario"
    )
    period = forms.ChoiceField(
        choices=[('morning', 'Mañana'), ('afternoon', 'Tarde')],
        label="Período"
    )
    hours = forms.FloatField(
        label="Horas a recuperar",
        min_value=0
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
    Formulario base para las preferencias diarias (campos comunes: morning, afternoon y cont).
    """
    class Meta:
        fields = ['morning', 'afternoon', 'sede']
        labels = {
            'morning': 'Mañana',
            'afternoon': 'Tarde',
            'sede': 'Sede'
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
