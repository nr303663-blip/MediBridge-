from django.contrib import admin
from .models import HospitalInfo, Department, Facility, InsurancePartner, Testimonial

admin.site.register(HospitalInfo)
admin.site.register(Department)
admin.site.register(Facility)
admin.site.register(InsurancePartner)
admin.site.register(Testimonial)
