from django.urls import path
from . import views

urlpatterns = [
    path('patients/dashboard/', views.patient_dashboard, name='patient_dashboard'),
]
