from django.urls import path
from . import views

urlpatterns = [
    path('register/doctor/', views.register_doctor_view, name='register_doctor'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/patient/', views.register_patient_view, name='register_patient'),
    # Add other URLs for patient details, odontogram actions etc.
    path('', views.login_view), # Redirect root to login for now
]
