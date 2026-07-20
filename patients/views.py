from django.shortcuts import render
from accounts.decorators import role_required


@role_required('patient')
def patient_dashboard(request):
    """
    Patient dashboard (Section 1: Patient module — Register/Login, Search
    Doctors, Book Appointment, Make Payment, Self Diagnostic, View Hospital
    Info). Appointment/payment data will be wired in during Phase 3.
    """
    patient = request.user.patient_profile
    appointments = patient.appointments.select_related('doctor__user').all()[:10]
    return render(request, 'patients/dashboard.html', {
        'patient': patient,
        'appointments': appointments,
    })
