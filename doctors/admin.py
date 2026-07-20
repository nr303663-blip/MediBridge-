from django.contrib import admin
from .models import Doctor, Specialization


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ('name',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'specialization', 'experience_years',
        'approval_status', 'is_available', 'consultation_fee'
    )
    list_filter = ('approval_status', 'is_available', 'specialization')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    actions = ['approve_doctors', 'decline_doctors']

    @admin.action(description="Approve selected doctors")
    def approve_doctors(self, request, queryset):
        queryset.update(approval_status=Doctor.ApprovalStatus.APPROVED)

    @admin.action(description="Decline selected doctors")
    def decline_doctors(self, request, queryset):
        queryset.update(approval_status=Doctor.ApprovalStatus.DECLINED)
