from django.conf import settings
from django.db import models
from hospital.models import Department


class Specialization(models.Model):
    """
    Maps to DB table `Doctor_Specialization (id, doctor_id, specialization)`
    at the lookup level — the list of specializations available in the
    system (e.g. Cardiology, Dermatology). Doctor <-> Specialization is
    linked via Doctor.specialization (FK) below, matching the roadmap's
    simple one-specialization-per-doctor model while still allowing the
    ML module (Section 3) to match predicted disease -> specialization.
    """
    name = models.CharField(max_length=150, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='specializations'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Doctor(models.Model):
    """
    Doctor Module (Section 2) + Doctors table (Section 7):
    `Doctors (id, user_id, specialization, experience, ...)`.

    Doctor accounts are created via the Authentication Module (a User
    with role='doctor') and are subject to the Approval Module before
    they can appear in search results / receive bookings.
    """

    class ApprovalStatus(models.TextChoices):
        PENDING = 'pending', 'Pending Approval'
        APPROVED = 'approved', 'Approved'
        DECLINED = 'declined', 'Declined'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile'
    )
    specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True, related_name='doctors'
    )
    experience_years = models.PositiveIntegerField(default=0)
    qualification = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    profile_photo = models.ImageField(upload_to='doctors/', blank=True, null=True)

    # Approval Module
    approval_status = models.CharField(
        max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING
    )

    # Availability (used by Appointment Module + ML recommendation engine)
    is_available = models.BooleanField(default=True)
    available_days = models.CharField(
        max_length=100, blank=True, help_text="Comma-separated, e.g. Mon,Tue,Wed"
    )
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-experience_years']

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username} ({self.specialization})"

    @property
    def is_approved(self):
        return self.approval_status == self.ApprovalStatus.APPROVED
