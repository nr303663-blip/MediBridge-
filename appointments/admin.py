from django.contrib import admin
from .models import Appointment, Notification
from .services import approve_appointment, decline_appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'date')
    search_fields = ('patient__user__username', 'doctor__user__username')
    actions = ['admin_approve', 'admin_decline']

    @admin.action(description="Approve selected appointments")
    def admin_approve(self, request, queryset):
        for appt in queryset:
            approve_appointment(appt)

    @admin.action(description="Decline selected (auto-recommends new doctor)")
    def admin_decline(self, request, queryset):
        for appt in queryset:
            decline_appointment(appt)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel', 'is_read', 'created_at')
    list_filter = ('channel', 'is_read')
