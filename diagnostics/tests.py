from django.test import TestCase
from doctors.models import Specialization, Doctor
from accounts.models import User
from diagnostics.models import Symptom, Disease
from diagnostics import ml_engine


class DiagnosticsEngineTests(TestCase):
    def setUp(self):
        self.spec = Specialization.objects.create(name='Cardiology')
        self.fever = Symptom.objects.create(name='Fever')
        self.cough = Symptom.objects.create(name='Cough')
        self.chest_pain = Symptom.objects.create(name='Chest Pain')

        self.flu = Disease.objects.create(name='Flu', recommended_specialization=self.spec)
        self.flu.typical_symptoms.set([self.fever, self.cough])

        self.heart_condition = Disease.objects.create(name='Heart Condition', recommended_specialization=self.spec)
        self.heart_condition.typical_symptoms.set([self.chest_pain])

    def test_predicts_best_matching_disease(self):
        result = ml_engine.predict_disease([self.fever.id, self.cough.id])
        self.assertEqual(result.disease, self.flu)
        self.assertGreater(result.confidence, 0)

    def test_no_symptoms_returns_no_prediction(self):
        result = ml_engine.predict_disease([])
        self.assertIsNone(result.disease)
        self.assertEqual(result.confidence, 0.0)

    def test_recommend_doctor_matches_specialization(self):
        user = User.objects.create_user(username='doc1', email='d@x.com', password='pass12345', role=User.Role.DOCTOR)
        doctor = Doctor.objects.create(
            user=user, specialization=self.spec, approval_status=Doctor.ApprovalStatus.APPROVED, is_available=True
        )
        recommended = ml_engine.recommend_doctor(self.flu)
        self.assertEqual(recommended, doctor)
