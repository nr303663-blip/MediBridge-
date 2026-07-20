from django.shortcuts import render
from .models import HospitalInfo, Department, Facility, Testimonial, InsurancePartner
from doctors.models import Doctor


def home(request):
    """
    Public homepage (Hospital Information Module, Section 8):
    hero, about, departments, doctors preview, facilities, testimonials,
    contact/location. Falls back to sensible defaults if the admin
    hasn't filled in HospitalInfo yet, so the page never looks broken.
    """
    info = HospitalInfo.objects.first()
    departments = Department.objects.all()[:6]
    facilities = Facility.objects.all()[:4]
    testimonials = Testimonial.objects.all()[:3]
    insurance_partners = InsurancePartner.objects.all()[:6]
    featured_doctors = (
        Doctor.objects
        .filter(approval_status=Doctor.ApprovalStatus.APPROVED, is_available=True)
        .select_related('user', 'specialization')
        .order_by('-experience_years')[:6]
    )

    return render(request, 'hospital/home.html', {
        'info': info,
        'departments': departments,
        'facilities': facilities,
        'testimonials': testimonials,
        'insurance_partners': insurance_partners,
        'featured_doctors': featured_doctors,
    })


def about(request):
    info = HospitalInfo.objects.first()
    departments = Department.objects.all()
    facilities = Facility.objects.all()
    return render(request, 'hospital/about.html', {
        'info': info, 'departments': departments, 'facilities': facilities,
    })


def contact(request):
    info = HospitalInfo.objects.first()
    return render(request, 'hospital/contact.html', {'info': info})
