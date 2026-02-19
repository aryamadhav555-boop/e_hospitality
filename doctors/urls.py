from django.urls import path
from . import views

urlpatterns = [
    path('doctors/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]
