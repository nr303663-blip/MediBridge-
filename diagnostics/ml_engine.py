"""
ML Self-Diagnostic Module — prediction engine.

Roadmap (Section 3) specifies: Algorithm = Random Forest / Naive Bayes /
SVM, trained on a disease-symptom dataset, saved as a `.pkl` and loaded
by the backend. This module is built so that swap-in is a one-line
change: `predict_disease()` is the single entry point every view calls,
and its internals can be replaced with a real scikit-learn model
(`joblib.load('model.pkl')`) without touching any calling code.

Until a trained dataset is supplied, this uses a transparent, always-
available fallback: a symptom-overlap scorer against each Disease's
`typical_symptoms` reference set (essentially a hand-weighted Naive
Bayes prior). Confidence is comparable in spirit to a real classifier's
predict_proba() output.
"""

from dataclasses import dataclass
from typing import Optional

from .models import Disease, Symptom


@dataclass
class PredictionResult:
    disease: Optional[Disease]
    confidence: float  # 0.0 - 1.0
    ranked: list  # list of (Disease, score) tuples, best first


def extract_text_symptom_ids(text):
    lower_text = text.lower()
    ids = set()
    for symptom in Symptom.objects.all():
        phrase = symptom.name.lower()
        if phrase in lower_text:
            ids.add(symptom.id)
        else:
            for token in phrase.split():
                if token and token in lower_text:
                    ids.add(symptom.id)
                    break
    return ids


def predict_disease(symptom_ids, other_text='') -> PredictionResult:
    """
    symptom_ids: iterable of Symptom PKs the patient selected.
    other_text: optional user-entered free-text symptoms.

    Scoring: for each Disease with a non-empty typical_symptoms set,
    score = (matched symptoms) / (size of the larger of the two sets)
    — a Jaccard-style overlap so a disease with a non-empty typical
    symptoms set doesn't win just by being broad, and a patient selecting
    many irrelevant symptoms doesn't inflate the match either.
    """
    selected = set(symptom_ids)
    if other_text:
        selected |= extract_text_symptom_ids(other_text)

    if not selected:
        return PredictionResult(disease=None, confidence=0.0, ranked=[])

    scored = []
    diseases = Disease.objects.prefetch_related('typical_symptoms').all()
    for disease in diseases:
        typical = set(disease.typical_symptoms.values_list('id', flat=True))
        if not typical:
            continue
        matched = selected & typical
        union = selected | typical
        score = len(matched) / len(union) if union else 0.0
        if matched:
            scored.append((disease, score))

    scored.sort(key=lambda pair: pair[1], reverse=True)

    if not scored:
        return PredictionResult(disease=None, confidence=0.0, ranked=[])

    best_disease, best_score = scored[0]
    return PredictionResult(disease=best_disease, confidence=round(best_score, 2), ranked=scored[:5])


def recommend_doctor(disease: Disease):
    """
    Given a predicted Disease, find the best-matched available doctor:
    same specialization as the disease's recommended_specialization,
    approved, available, ranked by experience (Section 3 flow step 4).
    """
    if not disease or not disease.recommended_specialization_id:
        return None

    from doctors.models import Doctor
    return (
        Doctor.objects
        .filter(
            specialization=disease.recommended_specialization,
            approval_status=Doctor.ApprovalStatus.APPROVED,
            is_available=True,
        )
        .order_by('-experience_years')
        .first()
    )
