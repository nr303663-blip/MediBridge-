from django.conf import settings
from django.db import models
from doctors.models import Specialization, Doctor


class Symptom(models.Model):
    """Maps to DB table `Symptoms (id, name)`."""
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Disease(models.Model):
    """
    Maps to DB table `Diseases (id, name, description)`.
    Each disease maps to a recommended specialization so the ML
    pipeline can go: symptoms -> predicted disease -> specialization
    -> best-matched available doctor (Section 3 flow).
    """
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    recommended_specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='diseases'
    )
    typical_symptoms = models.ManyToManyField(
        Symptom, related_name='typical_of_diseases', blank=True,
        help_text="Reference symptom set used by the diagnostic engine to score this disease."
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DiagnosisRequest(models.Model):
    """
    Logs one run of the ML self-diagnostic flow:
    1. User selects basic symptoms
    2. ML model (Random Forest / Naive Bayes / SVM, trained offline,
       saved as .pkl and loaded by the diagnostics service layer)
       processes symptoms and predicts the most likely disease
    3. System recommends best-matched specialization & doctor
    4. Patient can book an appointment directly from the result
    """
    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE, related_name='diagnosis_requests'
    )
    symptoms = models.ManyToManyField(Symptom, related_name='diagnosis_requests')
    predicted_disease = models.ForeignKey(
        Disease, on_delete=models.SET_NULL, null=True, blank=True, related_name='predictions'
    )
    confidence_score = models.FloatField(
        null=True, blank=True, help_text="Model's prediction confidence (0-1)."
    )
    recommended_doctor = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='ml_recommendations'
    )
    other_symptoms = models.TextField(blank=True, default='', help_text="Additional free-text symptoms entered by the patient.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Diagnosis for {self.patient} -> {self.predicted_disease}"
