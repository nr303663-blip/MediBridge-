from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'contact_number', 'blood_group')
    search_fields = ('user__username', 'user__email', 'contact_number')
    list_filter = ('gender', 'blood_group')
