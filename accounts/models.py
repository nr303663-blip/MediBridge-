from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model backing the Authentication Module.
    Roles: patient, doctor, admin -> drives role-based access control
    across the whole system (Section 2: Authentication Module).

    Maps to DB table `Users (id, name, email, password, role)` from the
    roadmap's database structure (Section 7). `username`/`password` are
    inherited from AbstractUser; `email` is made unique + required here.
    """

    class Role(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        DOCTOR = 'doctor', 'Doctor'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.PATIENT)
    phone_number = models.CharField(max_length=20, blank=True)
    is_active_account = models.BooleanField(
        default=True,
        help_text="Soft flag admins can use to disable an account without deleting it."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    @property
    def is_patient(self):
        return self.role == self.Role.PATIENT

    @property
    def is_doctor(self):
        return self.role == self.Role.DOCTOR

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN
