from django.shortcuts import render, get_object_or_404
from accounts.decorators import approved_doctor_required, role_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import Doctor, Specialization


def doctor_search(request):
    """
    Doctor search/listing page. Anyone can browse (Section 1: Patient
    module -> 'Search Doctors'); only approved & available doctors show.
    Supports filtering by specialization and free-text name search.
    """
    doctors = (
        Doctor.objects
        .filter(approval_status=Doctor.ApprovalStatus.APPROVED, is_available=True)
        .select_related('user', 'specialization')
        .order_by('-experience_years')
    )

    query = request.GET.get('q', '').strip()
    spec_id = request.GET.get('specialization', '').strip()

    if query:
        doctors = doctors.filter(user__first_name__icontains=query) | doctors.filter(
            user__last_name__icontains=query
        )
    if spec_id:
        doctors = doctors.filter(specialization_id=spec_id)

    specializations = Specialization.objects.all()

    return render(request, 'doctors/search.html', {
        'doctors': doctors.distinct(),
        'specializations': specializations,
        'query': query,
        'selected_spec': spec_id,
    })


def doctor_detail(request, doctor_id):
    """Doctor profile page with a 'Book Appointment' call-to-action."""
    doctor = get_object_or_404(
        Doctor.objects.select_related('user', 'specialization'),
        pk=doctor_id,
        approval_status=Doctor.ApprovalStatus.APPROVED,
    )
    return render(request, 'doctors/detail.html', {'doctor': doctor})


@approved_doctor_required
def doctor_dashboard(request):
    """
    Doctor dashboard (Section 1: Doctor module — Login to Dashboard, View
    Appointments, Approve/Decline, Manage Profile, View Patient History).
    Only reachable once an admin has approved the doctor's account.
    """
    doctor = request.user.doctor_profile
    appointments = doctor.appointments.select_related('patient__user').all()[:10]
    return render(request, 'doctors/dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
    })
