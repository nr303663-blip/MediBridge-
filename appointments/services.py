"""
Business logic for the Appointment + Approval + Notification modules.

Implements the roadmap's flowchart (Section 1):

    Doctor declines appointment
            |
            v
    IF APPOINTMENT DECLINED:
      Auto-recommend another suitable doctor & notify patient
"""

from django.db import transaction
from django.utils import timezone

from doctors.models import Doctor
from .models import Appointment, Notification


def find_alternative_doctor(appointment: Appointment):
    """
    Suitable doctor = same specialization as the declined doctor,
    approved, available, not the same doctor, ranked by experience.
    """
    return (
        Doctor.objects
        .filter(
            specialization=appointment.doctor.specialization,
            approval_status=Doctor.ApprovalStatus.APPROVED,
            is_available=True,
        )
        .exclude(pk=appointment.doctor_id)
        .order_by('-experience_years')
        .first()
    )


@transaction.atomic
def decline_appointment(appointment: Appointment, reason: str = ""):
    """
    Called when a doctor declines an appointment from their dashboard.

    1. Mark the original appointment as declined.
    2. Look for another suitable doctor (same specialization, approved,
       available).
    3. If found, create a new PENDING appointment with that doctor at
       the same requested date/time, linked back via `rebooked_from`.
    4. Notify the patient either way.
    """
    appointment.status = Appointment.Status.DECLINED
    appointment.save(update_fields=['status', 'updated_at'])

    alternative = find_alternative_doctor(appointment)

    if alternative:
        new_appointment = Appointment.objects.create(
            patient=appointment.patient,
            doctor=alternative,
            date=appointment.date,
            time=appointment.time,
            reason=appointment.reason,
            status=Appointment.Status.PENDING,
            payment_status=appointment.payment_status,
            rebooked_from=appointment,
        )
        message = (
            f"Dr. {appointment.doctor.user.get_full_name()} declined your appointment "
            f"request for {appointment.date} at {appointment.time}. "
            f"We've automatically booked you with Dr. {alternative.user.get_full_name()} "
            f"({alternative.specialization}) for the same slot, pending their approval."
        )
    else:
        new_appointment = None
        message = (
            f"Dr. {appointment.doctor.user.get_full_name()} declined your appointment "
            f"request for {appointment.date} at {appointment.time}. "
            f"No alternative {appointment.doctor.specialization} doctor is available "
            f"right now — please try booking a different time slot."
        )

    Notification.objects.create(
        user=appointment.patient.user,
        appointment=new_appointment or appointment,
        channel=Notification.Channel.IN_APP,
        message=message,
    )

    return new_appointment


@transaction.atomic
def approve_appointment(appointment: Appointment):
    appointment.status = Appointment.Status.APPROVED
    appointment.save(update_fields=['status', 'updated_at'])

    Notification.objects.create(
        user=appointment.patient.user,
        appointment=appointment,
        channel=Notification.Channel.IN_APP,
        message=(
            f"Good news! Dr. {appointment.doctor.user.get_full_name()} approved your "
            f"appointment for {appointment.date} at {appointment.time}."
        ),
    )
    return appointment
