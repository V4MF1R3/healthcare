from django.contrib import admin
from django.urls import path
from api.views import (
    RegisterView, PatientListCreateView, PatientDetailView,
    DoctorListCreateView, DoctorDetailView, MappingListCreateView, MappingDetailView,
    PatientDoctorMappingByPatientView, LoginView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Patients
    path('api/patients/', PatientListCreateView.as_view(), name='patients'),
    path('api/patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),

    # Doctors
    path('api/doctors/', DoctorListCreateView.as_view(), name='doctors'),
    path('api/doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),

    # Patient-Doctor Mappings
    path('api/mappings/', MappingListCreateView.as_view(), name='mappings'),
    path('api/mappings/<int:pk>/', MappingDetailView.as_view(), name='mapping-detail'),  # For DELETE
    path('api/mappings/patient/<int:patient_id>/', PatientDoctorMappingByPatientView.as_view(), name='mappings-by-patient'),
]