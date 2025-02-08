# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from datetime import datetime
from .models import monday
from .forms import UserPreferencesForm
from django.contrib.auth.decorators import login_required
import pytz

def index_view(request):
    if request.user.is_authenticated:
        # Zona horaria de Bogotá
        zona_bogota = pytz.timezone("America/Bogota")
        fecha_actual = datetime.now(zona_bogota)  # Obtiene la fecha y hora de Bogotá

        # Obtener el día de la semana (0 = lunes, 6 = domingo)
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dia_actual = fecha_actual.weekday()  # Devuelve 0 (Lunes) a 6 (Domingo)
        nombre_dia = dias_semana[dia_actual]  # Convertir número en nombre del día

        # Determinar si es fin de semana
        if dia_actual == 5 or dia_actual == 6:  # 5 = Sábado, 6 = Domingo
            mensaje = "🎉 ¡Es fin de semana! Disfruta tu descanso. 🚀"
        else:
            mensaje = "💼 Es un día de semana. ¡A trabajar duro!"

        return render(request, "app/index.html", {
            "dia": nombre_dia,
            "hora": fecha_actual.strftime("%I:%M %p"),  # Formato de hora 12h AM/PM
            "mensaje": mensaje
        })
    else:
        return redirect("login")  # Redirige a la vista de login si no está autenticado

@login_required
def user_preferences_view(request):
    preferences, created = monday.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserPreferencesForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirige a una página de éxito
    else:
        form = UserPreferencesForm(instance=preferences)

    return render(request, 'app/preferences.html', {'form': form})

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Crea el usuario
            messages.success(request, "Tu cuenta ha sido creada. ¡Ahora inicia sesión!")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "app/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Has iniciado sesión exitosamente.")
            return redirect("index")
        else:
            messages.error(request, "Nombre de usuario o contraseña no válidos.")
    return render(request, "app/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión.")
    return redirect("login")
