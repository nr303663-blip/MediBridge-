from django.db import models
from appointments.models import Appointment


class Payment(models.Model):
    """
    Maps to DB table `Payments (id, appointment_id, amount, method,
    status, transaction_id)` (Section 7).

    Supports the methods listed in Section 4: Cards (Credit/Debit),
    UPI/Net Banking, Wallets, Cash on Delivery — via Stripe, Razorpay,
    PayPal, Paytm or UPI, all behind one abstraction so the frontend
    doesn't care which gateway processed it.
    """

    class Method(models.TextChoices):
        CARD = 'card', 'Credit/Debit Card'
        UPI = 'upi', 'UPI'
        NETBANKING = 'netbanking', 'Net Banking'
        WALLET = 'wallet', 'Wallet'
        COD = 'cod', 'Cash on Delivery'

    class Gateway(models.TextChoices):
        STRIPE = 'stripe', 'Stripe'
        RAZORPAY = 'razorpay', 'Razorpay'
        PAYPAL = 'paypal', 'PayPal'
        PAYTM = 'paytm', 'Paytm'
        NONE = 'none', 'N/A (Cash on Delivery)'

    class Status(models.TextChoices):
        INITIATED = 'initiated', 'Initiated'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=15, choices=Method.choices)
    gateway = models.CharField(max_length=15, choices=Gateway.choices, default=Gateway.NONE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.INITIATED)
    transaction_id = models.CharField(max_length=150, blank=True, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.pk} - {self.amount} via {self.method} [{self.status}]"
