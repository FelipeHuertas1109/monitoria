# app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
import pytz
from .models import Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, Sede
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
import pytz
from .models import Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, Sede
from .forms import (
    UserRegisterForm, MondayForm, TuesdayForm, WednesdayForm,
    ThursdayForm, FridayForm, SaturdayForm, SundayForm
)

def index_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    zona_bogota = pytz.timezone("America/Bogota")
    fecha_actual = datetime.now(zona_bogota)
    
    dias_atributo = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    dias_display   = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dia_index = fecha_actual.weekday()  # 0 (Lunes) a 6 (Domingo)
    day_attr = dias_atributo[dia_index]
    nombre_dia = dias_display[dia_index]
    
    models_mapping = {
        "monday": Monday,
        "tuesday": Tuesday,
        "wednesday": Wednesday,
        "thursday": Thursday,
        "friday": Friday,
        "saturday": Saturday,
        "sunday": Sunday,
    }
    ModelClass = models_mapping[day_attr]
    preferences, created = ModelClass.objects.get_or_create(user=request.user)
    
    # Si last_mark_date es None o es un día distinto, reiniciamos los flags de marcado y autorización
    if preferences.last_mark_date != fecha_actual.date():
        preferences.morning_marked = False
        preferences.afternoon_marked = False
        preferences.morning_authorized = False
        preferences.afternoon_authorized = False
        preferences.last_mark_date = fecha_actual.date()
        preferences.save()
    
    time_period = "morning" if fecha_actual.hour < 12 else "afternoon"
    
    if time_period == "morning":
        mostrar_boton = preferences.morning and preferences.morning_authorized and not preferences.morning_marked
    else:
        mostrar_boton = preferences.afternoon and preferences.afternoon_authorized and not preferences.afternoon_marked
    
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
        "mensaje": mensaje,
        "mostrar_boton": mostrar_boton,
    })


@login_required


def mark_work_view(request):
    if request.method == 'POST':
        zona_bogota = pytz.timezone("America/Bogota")
        fecha_actual = datetime.now(zona_bogota)
        
        dias_atributo = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        models_mapping = {
            "monday": Monday,
            "tuesday": Tuesday,
            "wednesday": Wednesday,
            "thursday": Thursday,
            "friday": Friday,
            "saturday": Saturday,
            "sunday": Sunday,
        }
        dia_index = fecha_actual.weekday()
        day_attr = dias_atributo[dia_index]
        ModelClass = models_mapping[day_attr]
        preferences, created = ModelClass.objects.get_or_create(user=request.user)
        
        time_period = "morning" if fecha_actual.hour < 12 else "afternoon"
        
        if time_period == "morning":
            if preferences.morning_marked:
                messages.info(request, "Ya has marcado en la mañana.")
            else:
                # Se usa el valor configurable (por defecto 4)
                preferences.cont += preferences.morning_hours
                preferences.morning_marked = True
                preferences.save()
                messages.success(request, "Has marcado tu chamba de la mañana.")
        else:
            if preferences.afternoon_marked:
                messages.info(request, "Ya has marcado en la tarde.")
            else:
                # Se usa el valor configurable (por defecto 4)
                preferences.cont += preferences.afternoon_hours
                preferences.afternoon_marked = True
                preferences.save()
                messages.success(request, "Has marcado tu chamba de la tarde.")
        
        return redirect("index")
    return redirect("index")

@login_required
def add_preferences_view(request):
    """
    Vista para agregar o editar las preferencias de TODOS los días en una misma página.
    Se usan formularios con prefijos para evitar conflictos.
    """
    monday, _    = Monday.objects.get_or_create(user=request.user)
    tuesday, _   = Tuesday.objects.get_or_create(user=request.user)
    wednesday, _ = Wednesday.objects.get_or_create(user=request.user)
    thursday, _  = Thursday.objects.get_or_create(user=request.user)
    friday, _    = Friday.objects.get_or_create(user=request.user)
    saturday, _  = Saturday.objects.get_or_create(user=request.user)
    sunday, _    = Sunday.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        monday_form    = MondayForm(request.POST, instance=monday, prefix='mon')
        tuesday_form   = TuesdayForm(request.POST, instance=tuesday, prefix='tue')
        wednesday_form = WednesdayForm(request.POST, instance=wednesday, prefix='wed')
        thursday_form  = ThursdayForm(request.POST, instance=thursday, prefix='thu')
        friday_form    = FridayForm(request.POST, instance=friday, prefix='fri')
        saturday_form  = SaturdayForm(request.POST, instance=saturday, prefix='sat')
        sunday_form    = SundayForm(request.POST, instance=sunday, prefix='sun')
        
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
            
            return redirect('add')
    else:
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

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
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
            if user.is_superuser:
                return redirect("authorize_users")
            else:
                return redirect("index")
        else:
            messages.error(request, "Nombre de usuario o contraseña no válidos.")
    return render(request, "app/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión.")
    return redirect("login")

@login_required
def authorize_users_view(request):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect("index")
    
    # Determinar el día actual en la zona de Bogotá
    zona_bogota = pytz.timezone("America/Bogota")
    fecha_actual = datetime.now(zona_bogota)
    
    dias_atributo = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    dias_display   = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dia_index = fecha_actual.weekday()
    day_attr = dias_atributo[dia_index]
    nombre_dia = dias_display[dia_index]
    
    models_mapping = {
        "monday": Monday,
        "tuesday": Tuesday,
        "wednesday": Wednesday,
        "thursday": Thursday,
        "friday": Friday,
        "saturday": Saturday,
        "sunday": Sunday,
    }
    ModelClass = models_mapping[day_attr]
    
    # Obtener el registro Sede del superusuario y construir la lista de sedes permitidas
    try:
        sede_super = Sede.objects.get(user=request.user)
    except Sede.DoesNotExist:
        messages.error(request, "No se encontró la configuración de sedes para el superusuario.")
        return redirect("index")
    
    allowed_sedes = []
    if sede_super.barcelona:
        allowed_sedes.append("Barcelona")
    if sede_super.san_antonio:
        allowed_sedes.append("San Antonio")
    
    # Filtrar las preferencias:
    # - Si el usuario tiene chamba en la mañana, su campo sede_morning debe estar en allowed_sedes.
    # - Si tiene chamba en la tarde, su campo sede_afternoon debe estar en allowed_sedes.
    preferences_list = ModelClass.objects.filter(
        (Q(morning=True) & Q(sede_morning__in=allowed_sedes)) |
        (Q(afternoon=True) & Q(sede_afternoon__in=allowed_sedes))
    ).order_by('user__username')
    nombre_sede = ""

    if sede_super.barcelona:
       nombre_sede = "Barcelona"
    elif sede_super.san_antonio:
       nombre_sede = "San Antonio"
    else:
       nombre_sede = "Barcelona y San Antonio"
    
    return render(request, "app/authorize_users.html", {
        "nombre_dia": nombre_dia,
        "nombre_sede": nombre_sede,
        "preferences_list": preferences_list,
    })

@login_required
def authorize_mark_view(request, pref_id, period, action):
    """
    Procesa la autorización o desautorización de un período para una preferencia en particular.
    Solo el superusuario puede realizar esta acción.
    
    Parámetros:
      - pref_id: ID de la preferencia.
      - period: 'morning' o 'afternoon'.
      - action: 'authorize' para autorizar o 'deauthorize' para desautorizar.
    """
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para acceder a esta acción.")
        return redirect("index")
    
    if period not in ['morning', 'afternoon']:
        messages.error(request, "Período no válido.")
        return redirect("authorize_users")
    
    zona_bogota = pytz.timezone("America/Bogota")
    fecha_actual = datetime.now(zona_bogota)
    
    dias_atributo = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    dia_index = fecha_actual.weekday()
    day_attr = dias_atributo[dia_index]
    
    models_mapping = {
        "monday": Monday,
        "tuesday": Tuesday,
        "wednesday": Wednesday,
        "thursday": Thursday,
        "friday": Friday,
        "saturday": Saturday,
        "sunday": Sunday,
    }
    ModelClass = models_mapping[day_attr]
    
    try:
        preference = ModelClass.objects.get(id=pref_id)
    except ModelClass.DoesNotExist:
        messages.error(request, "No se encontró la preferencia.")
        return redirect("authorize_users")
    
    if action == "authorize":
        if period == "morning":
            preference.morning_authorized = True
        else:
            preference.afternoon_authorized = True
        messages.success(request, f"Se autorizó {period} para el usuario {preference.user.username}.")
    elif action == "deauthorize":
        if period == "morning":
            preference.morning_authorized = False
        else:
            preference.afternoon_authorized = False
        messages.success(request, f"Se desautorizó {period} para el usuario {preference.user.username}.")
    else:
        messages.error(request, "Acción no válida.")
        return redirect("authorize_users")
    
    preference.save()
    return redirect("authorize_users")

# app/views.py (al final del archivo)
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

@login_required
def report_users_view(request):
    """
    Vista para el superusuario que muestra una lista de todos los usuarios.
    Cada usuario tiene un botón "Reporte" para ver el total de horas acumuladas.
    """
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect("index")
    
    users = User.objects.all().order_by('username')
    return render(request, "app/report_users.html", {"users": users})

@login_required
def user_report_view(request, user_id):
    """
    Vista que muestra el reporte para un usuario en particular.
    Obtiene los registros de cada día (creándolos si no existen) y suma el total de horas.
    """
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect("index")
    
    user_obj = get_object_or_404(User, pk=user_id)
    
    # Para cada día, obtener (o crear) la instancia y tomar el valor de 'cont'
    monday_obj, _    = Monday.objects.get_or_create(user=user_obj)
    tuesday_obj, _   = Tuesday.objects.get_or_create(user=user_obj)
    wednesday_obj, _ = Wednesday.objects.get_or_create(user=user_obj)
    thursday_obj, _  = Thursday.objects.get_or_create(user=user_obj)
    friday_obj, _    = Friday.objects.get_or_create(user=user_obj)
    saturday_obj, _  = Saturday.objects.get_or_create(user=user_obj)
    sunday_obj, _    = Sunday.objects.get_or_create(user=user_obj)
    
    # Crear una lista con el desglose por día (nombre y horas)
    days = [
        ("Lunes", monday_obj.cont),
        ("Martes", tuesday_obj.cont),
        ("Miércoles", wednesday_obj.cont),
        ("Jueves", thursday_obj.cont),
        ("Viernes", friday_obj.cont),
        ("Sábado", saturday_obj.cont),
        ("Domingo", sunday_obj.cont),
    ]
    
    # Calcular el total de horas
    total = sum(hours for _, hours in days)
    
    context = {
        "user_obj": user_obj,
        "days": days,
        "total": total,
    }
    return render(request, "app/user_report.html", context)

from .forms import RecoverHoursForm
from django.contrib.auth.models import User
@login_required
def recover_hours_view(request):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para acceder a esta acción.")
        return redirect("index")
    
    if request.method == 'POST':
        form = RecoverHoursForm(request.POST)
        if form.is_valid():
            selected_user = form.cleaned_data['user']
            period = form.cleaned_data['period']
            hours = form.cleaned_data['hours']
            
            # Usar la zona horaria de Bogotá y determinar el día actual
            zona_bogota = pytz.timezone("America/Bogota")
            fecha_actual = datetime.now(zona_bogota)
            dias_atributo = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            dia_index = fecha_actual.weekday()
            day_attr = dias_atributo[dia_index]
            
            models_mapping = {
                "monday": Monday,
                "tuesday": Tuesday,
                "wednesday": Wednesday,
                "thursday": Thursday,
                "friday": Friday,
                "saturday": Saturday,
                "sunday": Sunday,
            }
            ModelClass = models_mapping[day_attr]
            record, created = ModelClass.objects.get_or_create(user=selected_user)
            
            # Actualizar el registro según el período seleccionado
            if period == "morning":
                record.morning = True
                record.morning_authorized = True
                record.morning_marked = False
            else:
                record.afternoon = True
                record.afternoon_authorized = True
                record.afternoon_marked = False
            
            # Sumar las horas a recuperar
            record.cont += hours
            record.save()
            
            messages.success(
                request,
                f"Se han recuperado {hours} horas para el usuario {selected_user.username} en el período { 'Mañana' if period=='morning' else 'Tarde' }."
            )
            return redirect("authorize_users")
    else:
        form = RecoverHoursForm()
    
    return render(request, "app/recover_hours.html", {"form": form})

# app/views.py

@login_required
def update_hours_view(request, pref_id, period):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para acceder a esta acción.")
        return redirect("authorize_users")
    
    if request.method == "POST":
        new_hours = request.POST.get("hours")
        try:
            new_hours = float(new_hours)
        except (ValueError, TypeError):
            messages.error(request, "Valor de horas no válido.")
            return redirect("authorize_users")
        
        # Determinar el registro correspondiente al día actual
        zona_bogota = pytz.timezone("America/Bogota")
        fecha_actual = datetime.now(zona_bogota)
        dias_atributo = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        dia_index = fecha_actual.weekday()
        day_attr = dias_atributo[dia_index]
        models_mapping = {
            "monday": Monday,
            "tuesday": Tuesday,
            "wednesday": Wednesday,
            "thursday": Thursday,
            "friday": Friday,
            "saturday": Saturday,
            "sunday": Sunday,
        }
        ModelClass = models_mapping[day_attr]
        try:
            record = ModelClass.objects.get(id=pref_id)
        except ModelClass.DoesNotExist:
            messages.error(request, "Registro no encontrado.")
            return redirect("authorize_users")
        
        if period == "morning":
            record.morning_hours = new_hours
        elif period == "afternoon":
            record.afternoon_hours = new_hours
        else:
            messages.error(request, "Período no válido.")
            return redirect("authorize_users")
        
        # Recalcular el total acumulado en 'cont'
        new_cont = 0
        if record.morning_marked:
            new_cont += record.morning_hours
        if record.afternoon_marked:
            new_cont += record.afternoon_hours
        record.cont = new_cont
        
        record.save()
        messages.success(
            request,
            f"Se actualizó las horas de { 'Mañana' if period=='morning' else 'Tarde' } a {new_hours} para {record.user.username}. " +
            "El total acumulado se ha recalculado."
        )
    return redirect("authorize_users")

@login_required
def work_students_view(request):
    """
    Vista que muestra a los estudiantes de ambos turnos (mañana y tarde)
    que tienen chamba el día actual.
    """
    zona_bogota = pytz.timezone("America/Bogota")
    fecha_actual = datetime.now(zona_bogota)
    
    # Determinar el día de la semana
    dias_atributo = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    dias_display   = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dia_index = fecha_actual.weekday()
    day_attr = dias_atributo[dia_index]
    nombre_dia = dias_display[dia_index]
    
    # Mapeo para obtener el modelo correspondiente al día actual
    models_mapping = {
        "monday": Monday,
        "tuesday": Tuesday,
        "wednesday": Wednesday,
        "thursday": Thursday,
        "friday": Friday,
        "saturday": Saturday,
        "sunday": Sunday,
    }
    ModelClass = models_mapping[day_attr]
    
    # Se seleccionan los estudiantes que tienen chamba en la mañana o en la tarde
    work_students = ModelClass.objects.filter(
        Q(morning=True) | Q(afternoon=True)
    ).order_by('user__username')
    
    context = {
        "nombre_dia": nombre_dia,
        "work_students": work_students,
    }
    
    return render(request, "app/work_students.html", context)