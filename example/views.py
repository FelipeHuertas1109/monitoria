# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from datetime import datetime
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

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
from .forms import (
    MondayForm, TuesdayForm, WednesdayForm,
    ThursdayForm, FridayForm, SaturdayForm, SundayForm
)

@login_required
def add_preferences_view(request):
    """
    Vista para agregar o editar las preferencias de todos los días en una misma página.
    La URL es /add/.
    """
    # Se obtienen o crean las instancias para cada día asociadas al usuario autenticado.
    monday, _   = Monday.objects.get_or_create(user=request.user)
    tuesday, _  = Tuesday.objects.get_or_create(user=request.user)
    wednesday, _= Wednesday.objects.get_or_create(user=request.user)
    thursday, _ = Thursday.objects.get_or_create(user=request.user)
    friday, _   = Friday.objects.get_or_create(user=request.user)
    saturday, _ = Saturday.objects.get_or_create(user=request.user)
    sunday, _   = Sunday.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Se instancian los formularios con los datos del POST y un prefix para diferenciarlos.
        monday_form    = MondayForm(request.POST, instance=monday, prefix='mon')
        tuesday_form   = TuesdayForm(request.POST, instance=tuesday, prefix='tue')
        wednesday_form = WednesdayForm(request.POST, instance=wednesday, prefix='wed')
        thursday_form  = ThursdayForm(request.POST, instance=thursday, prefix='thu')
        friday_form    = FridayForm(request.POST, instance=friday, prefix='fri')
        saturday_form  = SaturdayForm(request.POST, instance=saturday, prefix='sat')
        sunday_form    = SundayForm(request.POST, instance=sunday, prefix='sun')
        
        # Se valida que todos los formularios sean correctos.
        if (monday_form.is_valid() and tuesday_form.is_valid() and wednesday_form.is_valid() and
            thursday_form.is_valid() and friday_form.is_valid() and saturday_form.is_valid() and
            sunday_form.is_valid()):
            
            monday_form.save()
            tuesday_form.save()
            wednesday_form.save()
            thursday_form.save()
            friday_form.save()
            saturday_form.save()
            sunday_form.save()
            
            # Redirige a la misma URL o a otra página de éxito.
            return redirect('add')
    else:
        # En caso de GET se instancian los formularios con la instancia actual y un prefix.
        monday_form    = MondayForm(instance=monday, prefix='mon')
        tuesday_form   = TuesdayForm(instance=tuesday, prefix='tue')
        wednesday_form = WednesdayForm(instance=wednesday, prefix='wed')
        thursday_form  = ThursdayForm(instance=thursday, prefix='thu')
        friday_form    = FridayForm(instance=friday, prefix='fri')
        saturday_form  = SaturdayForm(instance=saturday, prefix='sat')
        sunday_form    = SundayForm(instance=sunday, prefix='sun')
    
    context = {
        'monday_form': monday_form,
        'tuesday_form': tuesday_form,
        'wednesday_form': wednesday_form,
        'thursday_form': thursday_form,
        'friday_form': friday_form,
        'saturday_form': saturday_form,
        'sunday_form': sunday_form,
    }
    return render(request, 'app/add_preferences.html', context)
