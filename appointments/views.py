from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from accounts.decorators import role_required, approved_doctor_required
from doctors.models import Doctor
from .models import Appointment
from .forms import BookAppointmentForm
from . import services


@role_required('patient')
def book_appointment(request, doctor_id):
    """
    Book Appointment (Section 1: Patient module). Creates a `pending`
    Appointment for the logged-in patient with the chosen doctor.
    Payment happens as a separate step after the doctor approves
    (see payments app) — matching the roadmap's Payment Module flow.
    """
    doctor = get_object_or_404(Doctor, pk=doctor_id, approval_status=Doctor.ApprovalStatus.APPROVED)
    patient = request.user.patient_profile

    if request.method == 'POST':
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = patient
            appointment.status = Appointment.Status.PENDING
            appointment.save()
            messages.success(
                request,
                f"Appointment request sent to Dr. {doctor.user.get_full_name()}. "
                f"You'll be notified once it's approved."
            )
            return redirect('patients:patients_home')
    else:
        form = BookAppointmentForm()

    return render(request, 'appointments/book.html', {'form': form, 'doctor': doctor})


@role_required('patient')
def my_appointments(request):
    patient = request.user.patient_profile
    appointments = patient.appointments.select_related('doctor__user', 'doctor__specialization').all()
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})


@role_required('patient')
@require_POST
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, patient=request.user.patient_profile)
    if appointment.status in (Appointment.Status.PENDING, Appointment.Status.APPROVED):
        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=['status', 'updated_at'])
        messages.info(request, "Appointment cancelled.")
    return redirect('appointments:my_appointments')


@approved_doctor_required
def doctor_appointments(request):
    doctor = request.user.doctor_profile
    appointments = doctor.appointments.select_related('patient__user').all()
    return render(request, 'appointments/doctor_appointments.html', {'appointments': appointments})


@approved_doctor_required
@require_POST
def approve_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, doctor=request.user.doctor_profile)
    services.approve_appointment(appointment)
    messages.success(request, "Appointment approved.")
    return redirect('appointments:doctor_appointments')


@approved_doctor_required
@require_POST
def decline_appointment_view(request, appointment_id):
    """
    Doctor declines -> triggers the roadmap's auto-recommend flow:
    services.decline_appointment() finds another suitable doctor,
    creates a new pending appointment for the patient with them, and
    sends a notification either way.
    """
    appointment = get_object_or_404(Appointment, pk=appointment_id, doctor=request.user.doctor_profile)
    new_appointment = services.decline_appointment(appointment)
    if new_appointment:
        messages.info(
            request,
            f"Declined. Patient was auto-rebooked with Dr. "
            f"{new_appointment.doctor.user.get_full_name()}."
        )
    else:
        messages.info(request, "Declined. No alternative doctor was available to auto-recommend.")
    return redirect('appointments:doctor_appointments')
