from django.contrib import admin
from .models import User, Patient, Doctor, PatientDoctorMapping
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(PatientDoctorMapping)
