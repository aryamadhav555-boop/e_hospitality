from django.shortcuts import render
from .models import Appointment

def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments/list.html', {'appointments': appointments})
