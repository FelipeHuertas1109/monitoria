# app/urls.py

from django.urls import path
from .views import (
    index_view, mark_work_view, add_preferences_view,
    register_view, login_view, logout_view,
    authorize_users_view, authorize_mark_view,
    report_users_view, user_report_view  # Importar las nuevas vistas
)

urlpatterns = [
    path('', index_view, name='index'),
    path('mark/', mark_work_view, name='mark_work'),
    path('add/', add_preferences_view, name='add'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # Rutas para autorización (ya existentes)
    path('authorize/', authorize_users_view, name='authorize_users'),
    path('authorize/<int:pref_id>/<str:period>/<str:action>/', authorize_mark_view, name='authorize_mark'),
    # Nuevas rutas para reportes
    path('report-users/', report_users_view, name='report_users'),
    path('report/<int:user_id>/', user_report_view, name='user_report'),
]
