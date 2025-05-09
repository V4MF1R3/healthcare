from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class UserTests(APITestCase):
    def test_register_user(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(username="testuser").exists())

class LoginTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

    def test_login_user(self):
        data = {
            "username": "testuser",
            "password": "password123"
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

class TokenRefreshTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        response = self.client.post('/api/auth/login/', {
            "username": "testuser",
            "password": "password123"
        })
        self.token = response.data['refresh']

    def test_token_refresh(self):
        response = self.client.post('/api/auth/token/refresh/', {'refresh': self.token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class PatientTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)
        patient_response = self.client.post('/api/patients/', {"name": "John Doe", "age": 30, "address": "123 Main Street"})
        self.patient = patient_response.data

    def test_create_patient(self):
        data = {
            "name": "John Doe",
            "age": 30,
            "address": "123 Main Street"
        }
        response = self.client.post('/api/patients/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "John Doe")

    def test_get_patients(self):
        response = self.client.get('/api/patients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_patient(self):
        response = self.client.get(f'/api/patients/{self.patient["id"]}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_patient(self):
        data = {"name": "Updated Name", "age": 35, "address": "456 New Street"}
        response = self.client.put(f'/api/patients/{self.patient["id"]}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Name")

    def test_delete_patient(self):
        response = self.client.delete(f'/api/patients/{self.patient["id"]}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class DoctorTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)
        doctor_response = self.client.post('/api/doctors/', {"name": "Dr. Smith", "specialization": "Cardiology"})
        self.doctor = doctor_response.data

    def test_create_doctor(self):
        data = {
            "name": "Dr. Smith",
            "specialization": "Cardiology"
        }
        response = self.client.post('/api/doctors/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Dr. Smith")

    def test_get_doctors(self):
        response = self.client.get('/api/doctors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_doctor(self):
        response = self.client.get(f'/api/doctors/{self.doctor["id"]}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_doctor(self):
        data = {"name": "Dr. Updated", "specialization": "Neurology"}
        response = self.client.put(f'/api/doctors/{self.doctor["id"]}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Dr. Updated")

    def test_delete_doctor(self):
        response = self.client.delete(f'/api/doctors/{self.doctor["id"]}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class PatientDoctorMappingTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

        patient_response = self.client.post('/api/patients/', {"name": "John Doe", "age": 30, "address": "123 Main Street"})
        self.patient = patient_response.data

        doctor_response = self.client.post('/api/doctors/', {"name": "Dr. Smith", "specialization": "Cardiology"})
        self.doctor = doctor_response.data

    def test_assign_doctor_to_patient(self):
        data = {
            "patient": self.patient["id"],
            "doctor": self.doctor["id"]
        }
        response = self.client.post('/api/mappings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_mappings(self):
        self.client.post('/api/mappings/', {"patient": self.patient["id"], "doctor": self.doctor["id"]})
        response = self.client.get('/api/mappings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_mappings_by_patient(self):
        self.client.post('/api/mappings/', {"patient": self.patient["id"], "doctor": self.doctor["id"]})
        response = self.client.get(f'/api/mappings/{self.patient["id"]}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_mapping(self):
        mapping_id = self.client.post('/api/mappings/', {"patient": self.patient["id"], "doctor": self.doctor["id"]}).data["id"]
        response = self.client.delete(f'/api/mappings/{mapping_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)