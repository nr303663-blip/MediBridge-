from django.db import models


class HospitalInfo(models.Model):
    """
    Maps to DB table `Hospital_Info (id, address, contact, departments, ...)`.
    Singleton-style: normally only one row exists (admin edits it via
    the Admin panel's "About Hospital" section).
    """
    name = models.CharField(max_length=255, default="MediBridge Hospital")
    logo = models.ImageField(upload_to='hospital/', blank=True, null=True)
    about = models.TextField(blank=True)
    address = models.TextField()
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    maps_embed_url = models.URLField(blank=True)
    working_hours = models.CharField(max_length=255, blank=True, help_text="e.g. Mon-Sat 8:00 AM - 8:00 PM")

    class Meta:
        verbose_name = "Hospital Info"
        verbose_name_plural = "Hospital Info"

    def __str__(self):
        return self.name


class Department(models.Model):
    """Departments & Services (Section 8)."""
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Icon class/name for frontend")

    def __str__(self):
        return self.name


class Facility(models.Model):
    """Facilities & Infrastructure (Section 8)."""
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='facilities/', blank=True, null=True)

    def __str__(self):
        return self.name


class InsurancePartner(models.Model):
    """Insurance Partners (Section 8)."""
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='insurance/', blank=True, null=True)

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    """Gallery & Testimonials (Section 8)."""
    patient_name = models.CharField(max_length=150)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.patient_name}"
