from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# forms.py
from django import forms
from .models import Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday

class BaseDayPreferenceForm(forms.ModelForm):
    """
    Formulario base para las preferencias diarias con los campos en común.
    """
    class Meta:
        fields = ['morning', 'afternoon', 'cont']

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
