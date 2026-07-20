from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor, Specialization


class AuthFlowTests(TestCase):
    def test_patient_signup_creates_user_and_profile(self):
        resp = self.client.post(reverse('accounts:patient_signup'), {
            'username': 'testpatient', 'first_name': 'Test', 'last_name': 'Patient',
            'email': 'test@patient.com', 'phone_number': '1234567890',
            'age': 30, 'gender': 'M',
            'password1': 'ComplexPass123!', 'password2': 'ComplexPass123!',
        })
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(username='testpatient')
        self.assertEqual(user.role, User.Role.PATIENT)
        self.assertTrue(Patient.objects.filter(user=user).exists())

    def test_doctor_signup_is_pending_by_default(self):
        resp = self.client.post(reverse('accounts:doctor_signup'), {
            'username': 'testdoctor', 'first_name': 'Test', 'last_name': 'Doctor',
            'email': 'test@doctor.com', 'phone_number': '1234567890',
            'qualification': 'MBBS', 'experience_years': 5,
            'password1': 'ComplexPass123!', 'password2': 'ComplexPass123!',
        })
        self.assertEqual(resp.status_code, 302)
        doctor = Doctor.objects.get(user__username='testdoctor')
        self.assertEqual(doctor.approval_status, Doctor.ApprovalStatus.PENDING)

    def test_pending_doctor_cannot_reach_dashboard(self):
        user = User.objects.create_user(username='pendingdoc', email='p@d.com', password='pass12345', role=User.Role.DOCTOR)
        Doctor.objects.create(user=user, approval_status=Doctor.ApprovalStatus.PENDING)
        self.client.login(username='pendingdoc', password='pass12345')
        resp = self.client.get(reverse('doctors:doctors_home'))
        self.assertEqual(resp.status_code, 302)  # redirected away, not into dashboard

    def test_login_redirects_by_role(self):
        user = User.objects.create_user(username='patient1', email='a@b.com', password='pass12345', role=User.Role.PATIENT)
        Patient.objects.create(user=user)
        self.client.login(username='patient1', password='pass12345')
        resp = self.client.get(reverse('accounts:dashboard_redirect'))
        self.assertRedirects(resp, reverse('patients:patients_home'))
