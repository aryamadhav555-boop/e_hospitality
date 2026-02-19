from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill #{self.id} - {self.patient.user.username}"

class Insurance(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=100)
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.provider_name

