from django.urls import path
from . import views

urlpatterns = [
    path('patients/dashboard/appointment/list/', views.appointment_list, name='appointment_list'),
]
