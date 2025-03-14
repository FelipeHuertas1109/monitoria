# app/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    index_view, mark_work_view, add_preferences_view,
    register_view, login_view, logout_view,
    authorize_users_view, authorize_mark_view,
    report_users_view, user_report_view,
      recover_hours_view, update_hours_view, work_students_view
)
from .forms import CustomPasswordResetForm, CustomSetPasswordForm


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
    path('recover_hours/', recover_hours_view, name='recover_hours'),
    # Nueva ruta para actualizar las horas
    path('update-hours/<int:pref_id>/<str:period>/', update_hours_view, name='update_hours'),
    path('work-students/', work_students_view, name='work_students'),
    # Rutas para resetear la contraseña
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="app/password_reset.html"), 
         name="reset_password"),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_sent.html"), 
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            form_class=CustomSetPasswordForm,
            template_name='app/password_reset_form.html'
        ),
         name="password_reset_confirm"),
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"), 
         name="password_reset_complete"),
]
