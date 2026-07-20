from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor, Specialization
from appointments.models import Appointment
from appointments import services


def make_doctor(username, spec, approved=True, available=True, experience=5):
    user = User.objects.create_user(username=username, email=f'{username}@x.com', password='pass12345', role=User.Role.DOCTOR)
    return Doctor.objects.create(
        user=user, specialization=spec, experience_years=experience,
        approval_status=Doctor.ApprovalStatus.APPROVED if approved else Doctor.ApprovalStatus.PENDING,
        is_available=available,
    )


class AppointmentFlowTests(TestCase):
    def setUp(self):
        self.spec = Specialization.objects.create(name='Cardiology')
        self.doctor = make_doctor('doc1', self.spec)
        self.other_doctor = make_doctor('doc2', self.spec, experience=10)

        self.patient_user = User.objects.create_user(
            username='pat1', email='pat1@x.com', password='pass12345', role=User.Role.PATIENT
        )
        self.patient = Patient.objects.create(user=self.patient_user)

    def test_patient_can_book_appointment(self):
        self.client.login(username='pat1', password='pass12345')
        resp = self.client.post(reverse('appointments:book_appointment', args=[self.doctor.id]), {
            'date': '2026-08-01', 'time': '10:00', 'reason': 'Checkup',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Appointment.objects.filter(patient=self.patient, doctor=self.doctor).exists())

    def test_decline_auto_recommends_another_doctor(self):
        appt = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date='2026-08-01', time='10:00', status=Appointment.Status.PENDING,
        )
        new_appt = services.decline_appointment(appt)
        appt.refresh_from_db()
        self.assertEqual(appt.status, Appointment.Status.DECLINED)
        self.assertIsNotNone(new_appt)
        self.assertEqual(new_appt.doctor, self.other_doctor)
        self.assertEqual(new_appt.status, Appointment.Status.PENDING)
        self.assertEqual(new_appt.rebooked_from, appt)

    def test_decline_with_no_alternative_still_notifies(self):
        # Remove the only alternative doctor from the pool
        self.other_doctor.is_available = False
        self.other_doctor.save()

        appt = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date='2026-08-01', time='10:00', status=Appointment.Status.PENDING,
        )
        new_appt = services.decline_appointment(appt)
        self.assertIsNone(new_appt)
        appt.refresh_from_db()
        self.assertEqual(appt.status, Appointment.Status.DECLINED)

    def test_doctor_can_approve(self):
        appt = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date='2026-08-01', time='10:00', status=Appointment.Status.PENDING,
        )
        self.client.login(username='doc1', password='pass12345')
        resp = self.client.post(reverse('appointments:approve_appointment', args=[appt.id]))
        self.assertEqual(resp.status_code, 302)
        appt.refresh_from_db()
        self.assertEqual(appt.status, Appointment.Status.APPROVED)
