from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required
from .forms import SymptomSelectForm
from .models import DiagnosisRequest
from . import ml_engine


@role_required('patient')
def select_symptoms(request):
    """
    Step 1 of Section 3's flow: "User selects basic symptoms".
    """
    if request.method == 'POST':
        form = SymptomSelectForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data['symptoms']
            other_symptoms = form.cleaned_data.get('other_symptoms', '').strip()
            result = ml_engine.predict_disease(symptoms.values_list('id', flat=True), other_symptoms)
            doctor = ml_engine.recommend_doctor(result.disease) if result.disease else None

            diagnosis = DiagnosisRequest.objects.create(
                patient=request.user.patient_profile,
                predicted_disease=result.disease,
                confidence_score=result.confidence,
                recommended_doctor=doctor,
                other_symptoms=other_symptoms,
            )
            diagnosis.symptoms.set(symptoms)

            return redirect('diagnostics:result', diagnosis_id=diagnosis.id)
    else:
        form = SymptomSelectForm()

    return render(request, 'diagnostics/select_symptoms.html', {'form': form})


@role_required('patient')
def result(request, diagnosis_id):
    """
    Steps 2-4: shows the ML prediction, confidence, and the
    best-matched recommended doctor with a direct "Book Appointment"
    link (Section 3: "Patient can book appointment with recommended
    doctor").
    """
    diagnosis = get_object_or_404(
        DiagnosisRequest, pk=diagnosis_id, patient=request.user.patient_profile
    )
    return render(request, 'diagnostics/result.html', {'diagnosis': diagnosis})


@role_required('patient')
def history(request):
    diagnoses = request.user.patient_profile.diagnosis_requests.select_related(
        'predicted_disease', 'recommended_doctor__user'
    ).all()
    return render(request, 'diagnostics/history.html', {'diagnoses': diagnoses})
