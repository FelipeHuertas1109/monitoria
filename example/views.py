# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import UserRegisterForm

def index_view(request):
    return render(request, "app/index.html")

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
