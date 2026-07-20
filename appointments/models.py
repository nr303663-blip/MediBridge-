from django.db import models
from patients.models import Patient
from doctors.models import Doctor


class Appointment(models.Model):
    """
    Maps to DB table `Appointments (id, patient_id, doctor_id, date, time,
    status, payment_status)` (Section 7).

    Status flow implements Section 1's system overview:
      pending -> approved / declined  (Doctor approves or declines)
      declined -> the system auto-recommends another suitable doctor
                  and notifies the patient (see services.py)
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        DECLINED = 'declined', 'Declined'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'
        RESCHEDULED = 'rescheduled', 'Rescheduled'

    class PaymentStatus(models.TextChoices):
        UNPAID = 'unpaid', 'Unpaid'
        PAID = 'paid', 'Paid'
        REFUNDED = 'refunded', 'Refunded'
        COD = 'cod', 'Cash on Delivery'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(blank=True, help_text="Patient-provided reason / symptoms summary")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)

    # Links back to an originating declined appointment, so the chain of
    # "declined -> auto-recommended -> rebooked" is fully auditable.
    rebooked_from = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='rebookings'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']
        indexes = [models.Index(fields=['doctor', 'date', 'time'])]

    def __str__(self):
        return f"{self.patient} -> {self.doctor} on {self.date} {self.time} [{self.status}]"


class Notification(models.Model):
    """
    Notification Module (Section 2): Email/SMS alerts, appointment
    reminders, and status notifications (e.g. doctor declined & a new
    doctor was auto-recommended).
    """

    class Channel(models.TextChoices):
        EMAIL = 'email', 'Email'
        SMS = 'sms', 'SMS'
        IN_APP = 'in_app', 'In-App'

    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='notifications'
    )
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications'
    )
    channel = models.CharField(max_length=10, choices=Channel.choices, default=Channel.IN_APP)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.user}: {self.message[:50]}"
