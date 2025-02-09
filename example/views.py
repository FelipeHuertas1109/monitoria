# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from datetime import datetime
import pytz
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
from .forms import (
    MondayForm, TuesdayForm, WednesdayForm,
    ThursdayForm, FridayForm, SaturdayForm, SundayForm
)

@login_required
def index_view(request):
    """
    Vista de inicio que muestra el mensaje de acuerdo al día actual y las preferencias configuradas
    para el usuario autenticado, utilizando la zona horaria de Bogotá.
    """
    # Zona horaria de Bogotá
    zona_bogota = pytz.timezone("America/Bogota")
    fecha_actual = datetime.now(zona_bogota)
    
    # Listas para obtener el atributo (nombre en inglés para acceder al objeto relacionado)
    # y el nombre para mostrar en español
    dias_atributo = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    dias_display = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    
    # Obtener el índice del día actual (0 = lunes, 6 = domingo)
    dia_index = fecha_actual.weekday()
    day_attr = dias_atributo[dia_index]   # por ejemplo, "sunday"
    nombre_dia = dias_display[dia_index]   # por ejemplo, "Domingo"
    
    # Mapeo de nombre de atributo al modelo correspondiente
    models_mapping = {
        "monday": Monday,
        "tuesday": Tuesday,
        "wednesday": Wednesday,
        "thursday": Thursday,
        "friday": Friday,
        "saturday": Saturday,
        "sunday": Sunday,
    }
    
    # Obtener (o crear si no existe) la instancia de preferencias para el día actual
    ModelClass = models_mapping[day_attr]
    preferences, created = ModelClass.objects.get_or_create(user=request.user)
    
    # Definir el período según la hora actual: si es antes de las 12 es "morning", sino "afternoon"
    time_period = "morning" if fecha_actual.hour < 12 else "afternoon"
    
    # Construir el mensaje de acuerdo a la preferencia marcada
    if getattr(preferences, time_period, False):
        if time_period == "morning":
            mensaje = f"Tienes chamba el {nombre_dia} en la mañana."
        else:
            mensaje = f"Tienes chamba el {nombre_dia} en la tarde."
    else:
        mensaje = "Hoy no chambeas."
    
    return render(request, "app/index.html", {
        "dia": nombre_dia,
        "hora": fecha_actual.strftime("%I:%M %p"),
        "mensaje": mensaje
    })

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
