# app/urls.py

from django.urls import path
from .views import (
    index_view, mark_work_view, add_preferences_view,
    register_view, login_view, logout_view,
    authorize_users_view, authorize_mark_view
)

urlpatterns = [
    path('', index_view, name='index'),
    path('mark/', mark_work_view, name='mark_work'),
    path('add/', add_preferences_view, name='add'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # Rutas para autorización (solo para superusuario)
    path('authorize/', authorize_users_view, name='authorize_users'),
    path('authorize/<int:pref_id>/<str:period>/', authorize_mark_view, name='authorize_mark'),
]
