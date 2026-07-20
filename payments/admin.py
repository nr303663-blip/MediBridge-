from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount', 'method', 'gateway', 'status', 'transaction_id', 'created_at')
    list_filter = ('method', 'gateway', 'status')
    search_fields = ('transaction_id',)
